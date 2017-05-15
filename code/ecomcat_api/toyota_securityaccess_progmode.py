from PyEcom import *
from config import *
import time, struct, sys

if __name__ == "__main__":
    #print "[*] Starting diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,35916)

    ECU = 0x7E0

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


##    for ecu_num, ecu_name in PriusECU.iteritems():
##        print "Trying security access for %s" % (ecu_name)
##        #security access
##        ret = ecom.security_access(ecu_num)
##
##    for ecu_sub_num, ecu_name in PriusMainECU.iteritems():
##        print "Trying security access for %s" % (ecu_name)
##        ret = ecom.security_access(0x750, ecu_sub_num)
