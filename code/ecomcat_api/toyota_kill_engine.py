from PyEcom import *
from config import *
import time, struct

if __name__ == "__main__":
    #print "[*] Starting diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,35916)

    ECU = 0x7E0

    #do security access
    ret = ecom.security_access(ECU)
    if ret == False:
        print "[!] [0x%04X] Security Access: FAILURE" % (ECU)
    else:            
        print "[*] [0x%04X] Security Access: Success" % (ECU)

    #Unsure but this happens 3x in the capture before diag programming mode
    #I think this may have to do w/ tellin other ECUs the one being reprogrammed
    #is going offline for a while and DO NOT set DTC codes
    for i in range(0, 3):
        ret = ecom.send_iso_tp_data(0x720, [0xA0, 0x27])

    ret = ecom.diagnostic_session(ECU, [0x10, 0x02])
    if ret == False:
        print "[!] [0x%04X] Programming Mode: FAILURE" % (ECU)
    else:
        print "[*] [0x%04X] Programming Mode: Sucess" % (ECU)

    for i in range(0, 10):
        ecom.send_iso_tp_data(0x7E0, [0x30, 0x1C, 0x00, 0x0F, 0xA5, 0x01])

