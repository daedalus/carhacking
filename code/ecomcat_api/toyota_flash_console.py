from PyEcom import *
from config import *
import time, struct, sys

def str_to_hexarr(val):
    payload = []
    for x in val:
        payload.append(ord(x))

    return payload

def nbo_int_to_bytearr(dword):
    arr = []
    arr.append(dword & 0xFF)
    arr.append((dword >> 8) & 0xFF)
    arr.append((dword >> 16) & 0xFF)
    arr.append((dword >> 24) & 0xFF)

#ECU which we'll be running the console
ECU = 0x7E0

#ECM LocationIDs
#T-0052-11.cuw LocationID=0002000100070720
#I'm not entirely sure of the ordering
lid1 = 0x20
lid2 = 0x07
lid3 = 0x01
lid4 = 0x00
lid5 = 0x02
lid6 = 0x00
lid7 = 0x07
lid8 = 0x00

#Client CAN ID which will be sending data/requests
CID = 0x0001

#Server CAN ID which will be receiving data/requests
SID = 0x0002

#val = ecom.toyota_targetdata_to_dword("424433493A4B4B4D")
#ECM Calibration 34715200
#T-0052-11.cuw 03_TargetData=424433493A4B4B4D
#target_data = 0xBC1F6FEF    
target_data = nbo_int_to_bytearr(0xBC1F6FEF)

if __name__ == "__main__":
    #print "[*] Starting diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(0,1)

    PREAMBLE = False

    #START PREAMBLE
    if PREAMBLE == True:

        #ret = ecom.send_iso_tp_data(0x7E1, [0x09, 0x00])

        #Supported PIDs (Bit Encoded)
        ret = ecom.send_iso_tp_data(ECU, [0x09, 0x00])

        #Get Calibration IDs
        ret = ecom.send_iso_tp_data(ECU, [0x09, 0x04])

        #do security access
        ret = ecom.security_access(ECU)
        if ret == False:
            print "[!] [0x%04X] Security Access: FAILURE" % (ECU)
            sys.exit(1)
            
        print "[*] [0x%04X] Security Access: Success" % (ECU)

        #Unsure but this happens 3x in the capture before diag programming mode
        #I think this may have to do w/ tellin other ECUs the one being reprogrammed
        #is going offline for a while and DO NOT set DTC codes
        for i in range(0, 3):
            ret = ecom.send_iso_tp_data(0x720, [0xA0, 0x27])

        #Grequires the to be in half-on state (power on, engine off)
        #Failure to be in the required mode will result in diagnostic session failing
        ret = ecom.diagnostic_session(ECU, [0x10, 0x02])
        if ret == False:
            print "[!] [0x%04X] Programming Mode: Failure" % (ECU)
            sys.exit(1)

        print "[*] [0x%04X] Programming Mode: Success" % (ECU)

        #These turn the 'check engine' light off. maybe puts ecu in offline mode?
        ecom.send_iso_tp_data(CID, [0x00])
        ecom.send_iso_tp_data(CID, [0x00])

        #This is the 'LocationID' see: T-0052-11.cuw
        ecom.send_iso_tp_data(CID, [lid1, lid2, lid3, lid4, lid5, lid6])
        ecom.send_iso_tp_data(CID, [lid7, lid8])

        #Send the targetdata/unlock to the ECU which will returns some kind of version number
        ecu_version_arr = ecom.send_iso_tp_data(CID, target_data, None, RcvAckData)

        #save the version as a string but also keep it as an array in case we need it
        ecu_version  = ''.join(chr(val) for val in ecu_version_arr)
        if(not ecu_version):
            print "[!] TargetData failed"
            sys.exit(1)

        print "[*] Current Version: %s" % (ecu_version)

        #ack that we got the data
        ecom.send_iso_tp_data(CID, [0x3C])

        #get the memory info i should really use this instead of the static
        #addresses that are assigned to the EcuBlock classes above
        mem_info = ecom.send_iso_tp_data(CID, [0x76], None, RcvAckData)

        #recv last response
        ret = ecom.recv_iso_tp_data(CID)

        print "[*] Acuired MemoryInfo %s" % (mem_info)     

    #start interactive CAN Flashing session
    while(1):
        print "1) Send Msg | Get Ack"
        print "2) Send Msg | Get AckData" 
        print "3) Send Repeated Character"
        print "4) Send Data from file"
        print "5) GetStatus"
        print "q) Quit"
        
        sys.stdout.write("Enter Choice: ")
        choice = sys.stdin.readline().strip()

        #Hit q to quit
        if(choice == "q" or choice == "Q"):
            break

        if choice == "1":
            sys.stdout.write("Enter Line: ")
            line = sys.stdin.readline().strip()

            payload = []
            for x in line.split(' '):
                payload.append(int(x, 16))
                
            ret = ecom.send_iso_tp_data(0x01, payload)
        elif choice == "2":
            sys.stdout.write("Enter Line: ")
            line = sys.stdin.readline().strip()

            payload = []
            for x in line.split(' '):
                payload.append(int(x, 16))
                
            ret = ecom.send_iso_tp_data(0x01, payload, None, RcvAckData)
        elif choice == "3":
            sys.stdout.write("Enter char,length: ")
            line = sys.stdin.readline().strip()

            data = line.split(',')
            val = ord(data[0].strip())

            length = int(data[1].strip(), 16)
            print "Len: %04X" % (length)

            payload = []
            for i in range(0, length):
                payload.append(val)

            ret = ecom.send_iso_tp_data(0x01, payload)
        elif choice == "4":
            sys.stdout.write("Enter file,offset,length: ")
            line = sys.stdin.readline().strip()

            data = line.split(',')
            fn = data[0].strip()
            f = None
            try:
                f = open(fn, "rb")
            except:
                if not f:
                    print "Bad filename: %s" % (fn)
                    continue

            offset = data[1].strip()
            offset = int(offset,16)

            length = data[2].strip()
            length = int(length, 16)
            
            f.seek(offset)

            file_data = f.read(length)
            payload = []
            for x in file_data:
                payload.append(ord(x))

            f.close()

            ret = ecom.send_iso_tp_data(0x01, payload)
        elif choice == "5":
            ret = ecom.toyota_getstatus(0x01)
            print ret
        elif choice == "q" or choice == "Q":
            break
        else:
            continue
