from PyEcom import *
from config import *
import time, struct, sys

if __name__ == "__main__":

    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(0,1)

    ECU = 0x7E0

    #Is CPU?
    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x00])

    #Get Calibration IDs
    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x04])

    #????
    ret = ecom.send_iso_tp_data(ECU, [0x13, 0x80])

    #Get VIN
    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x04])

    ret = ecom.security_access(ECU)
    if ret:
        print "[*] [0x%04X] Security Access: Success" % (ECU)

        #Unsure but this happens 3x in the capture before diag programming mode
        #I think this may have to do w/ tellin other ECUs the one being reprogrammed
        #is going offline for a while and DO NOT set DTC codes
        for i in range(0, 3):
            ret = ecom.send_iso_tp_data(0x720, [0xA0, 0x27])
                                        
        ret = ecom.diagnostic_session(ECU, [0x10, 0x02])
        if ret:
            print "[*] [0x%04X] Programming Mode: Success" % (ECU)

            ecom.send_iso_tp_data(0x01, [0x00])
            ecom.send_iso_tp_data(0x01, [0x00])

            #This is the 'LocationID' see: T-0052-11.cuw
            ecom.send_iso_tp_data(0x01, [0x20, 0x07, 0x01, 0x00, 0x02, 0x00])
            ecom.send_iso_tp_data(0x01, [0x07, 0x00])

            f = open("toyota_ecu.bin", "rb")

            while True:
                chunk = f.read(4)
                if not chunk:
                    break

                p1 = ord(chunk[0])
                p2 = ord(chunk[1])
                p3 = ord(chunk[2])
                p4 = ord(chunk[3])

                ecu_version = ecom.send_iso_tp_data(0x01, [p1, p2, p3, p4])
                if ecu_version:
                    print "FOUND MAGIC: %02X %02X %02X %02X" % (p1,p2,p3,p4)
                    break

            close(f)
