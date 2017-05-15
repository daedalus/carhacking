#This flasher only works for updating a ToyotaPrius Engine Control Module (ECM)
#from calibration 34715200 to calibration 34715300. It may be altered to work with
#other ECUs and versions since most will generally be the same
#Chris Valasek - cvalasek@gmail.com May 2013

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

    return arr 

class EcuBlock:
    def __init__(self, address, write_address, length):
        self.address = address
        self.write_address = write_address
        self.length = length 

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

#ClientID (described above in the LocationID)
CID = 0x01

#Attempt to reflash the 2010 Toyota Prius ECM (Engine Control Module)
ECU = 0x7E0

#ECU Block Addresses
ecu_b1 = EcuBlock(0x00000000, 0xFF000000, 0x1000)
ecu_b2 = EcuBlock(0xF7000100, 0xFF001000, None)

blocks = []
blocks.append(ecu_b1)
blocks.append(ecu_b2)

#val = ecom.toyota_targetdata_to_dword("424433493A4B4B4D")
#ECM Calibration 34715200
#T-0052-11.cuw 03_TargetData=424433493A4B4B4D
#target_data = 0xBC1F6FEF    
target_data = nbo_int_to_bytearr(0xBC1F6FEF)

if __name__ == "__main__":
    #print "[*] Starting diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(0,1) 

    #Set this to False if flashing fails and the script needs re-run
    PREAMBLE = False

    #flash binary
    f = open("toyota_ecm.bin", "rb")

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
    #END PREAMBLE


    ##### WriteBlocks #########
    ##### 1) CheckBlock #######
    ##### 2) EraseBlock #######
    ##### 3) WriteBlock 41 ####
    ##### 4) WriteBlock 45 ####
    ##### 5) InverifyBlock ####
    ##### 6) VerifyBlock ######
    for block in blocks: 

        #keep track of the total bytes written
        total_written = 0
        block_data = []

        addr_arr = nbo_int_to_bytearr(block.address)
        write_arr = nbo_int_to_bytearr(block.write_address)

        #read one chunk from the file
        chunk = f.read(0x400)
        if(not chunk):
            print "[!] Chunk could not be read"
            sys.exit(1)

        #CheckBlock
        ecom.send_iso_tp_data(CID, [0x36, addr_arr[0], addr_arr[1], addr_arr[2], addr_arr[3]])
        ret = ecom.toyota_loop_getstatus(CID, 0x10, 0x01)
        if(ret != ""):
            print "[!] CheckBlock Error: %02X" % (ret)
            sys.exit(1)

        #EraseBlock
        ecom.send_iso_tp_data(CID, [0x26, addr_arr[0], addr_arr[1], addr_arr[2], addr_arr[3]])
        ret = ecom.toyota_loop_getstatus(CID, 0x80)
        if(ret != ""):
            print "[!] EraseBlock Error: %02X" % (ret)
            sys.exit(1)

        #WriteBlock with address
        ecom.send_iso_tp_data(CID, [0x41])
        ecom.send_iso_tp_data(CID, write_arr)

        #make the bytes into an array
        chunk_arr = str_to_hexarr(chunk)

        #store all the data in this block for verification
        block_data += chunk_arr

        #send the data and wait for a good response
        ret = ecom.send_iso_tp_data(CID, chunk_arr)
        ret = ecom.toyota_loop_getstatus(CID, 0x40)
        if(ret != ""):
            print "[!] WriteBlock[0x41] Error: %02X" % (ret)
            print chunk_arr
            sys.exit(1) 

        total_written += 0x400

        #write the rest of the data
        while(True):
            if(block.length != None):
                if(total_written >= block.length):
                    break

            #read one chunk from the file
            chunk = f.read(0x400)
            if(not chunk):
                break

            #WriteBlock continued
            ecom.send_iso_tp_data(CID, [0x45])

            #make the bytes into an array
            chunk_arr = str_to_hexarr(chunk)

            #store all the data in this block for verification
            block_data += chunk_arr

            ret = ecom.send_iso_tp_data(CID, chunk_arr)
            ret = ecom.toyota_loop_getstatus(CID, 0x40)
            if(ret != ""):
                print "[!] WriteBlock[0x45] Error: %02X" % (ret)
                print chunk_arr
                sys.exit(1)

            time.sleep(0.05)

            total_written += 0x400

        #InVerifyBlock
        ecom.send_iso_tp_data(CID, [0x48, addr_arr[0], addr_arr[1], addr_arr[2], addr_arr[3]])
        ret = ecom.toyota_loop_getstatus(CID, 0x40)
        if(ret != ""):
            print "[!] InVerifyBlock Error: %02X" % (ret)
            print chunk_arr
            sys.exit(1)    

        #VerifyBlock
        ecom.send_iso_tp_data(CID, [0x16, addr_arr[0], addr_arr[1], addr_arr[2], addr_arr[3]])

        verified_chunks = total_written / 0x100
        vindex = 0
        for i in range(0, verified_chunks):
            verify_chunk = block_data[vindex:vindex+0x100]

            #write the 0x100 bytes to be verified
            ecom.send_iso_tp_data(CID, verify_chunk)

            #get an OK status
            ret = ecom.toyota_loop_getstatus(CID, 0x20)
            if(ret != ""):
                print "[!] VerifyBlock Error: %02X" % (ret)
                print verify_chunk
                sys.exit(1)             

            vindex += 0x100
            
    ####END OF FLASHING####
    ret = ecom.send_iso_tp_data(0x720, [0x80])

    #something
    ret = ecom.send_iso_tp_data(0x72F, [0x7F, 0x80, 0x11])

    #Supported PIDs (Bit Encoded)
    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x00])

    #Get Calibration IDs
    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x04])
