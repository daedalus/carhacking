from PyEcom import *
from config import *

if __name__ == "__main__":
    print "[*] Starting Prius diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(0,1)

    diag_req = [0x10, PriusDiagCode]

    for ecu_num, ecu_str in PriusECU.iteritems():
        
        print "DaigCheck...[0x%04X] => %s..." % (ecu_num, ecu_str)
        ret = ecom.diagnostic_session(ecu_num, diag_req)
        if(not ret):
            print "FAILED\n"
        else:
            print "SUCCEEDED!\n"

    for ecu_sub_num, ecu_str in PriusMainECU.iteritems():
        print "DiagCheck...[0x0750:0x%02X] => %s..." % (ecu_sub_num, ecu_str)
        ret = ecom.diagnostic_session(0x750, diag_req, ecu_sub_num)
        if(not ret):
            print "FAILED\n"
        else:
            print "SUCCEEDED!\n"
    
    
