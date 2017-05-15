from PyEcom import *
from config import *
import time, struct

if __name__ == "__main__":
    #print "[*] Starting diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,35916)

    #It looks like all commands for 'active tests' use the 0x30
    #service which is 'inputOutputControlByLocalIdentifier' (see ISO 14230/14229)

##    Clear DTC codes for all ECUs
##    for ecu_num, ecu_name in PriusECU.iteritems():
##            ecom.send_iso_tp_data(ecu_num, [0x04])
##            ecom.send_iso_tp_data(ecu_num, [0x14])

##    for ecu_sub_num, ecu_name in PriusMainECU.iteritems():
##            ecom.send_iso_tp_data(0x750, [0x04], ecu_sub_num)

    #Clear steering abnormalities history
    #ecom.send_iso_tp_data(0x7A1, [0xA6, 0x00])

    #Clear ABS history
    #ecom.send_iso_tp_data(0x7B0, [0xA6, 0x00])

    #AC Turn blower on 00-1F (00-31 decimal) [driving]
    #ecom.send_iso_tp_data(0x7C4, [0x30, 0x02, 0x00, 0x1F])

    #Combo Meter Fuel Empty + beep [driving]
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x01])

    #Combo Meter Fuel Empty
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x02])

    #Combo Meter Fuel Empty
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x04])    

    #Combo Meter Fuel 1/4 tank
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x08])

    #Combo Meter Fuel 1/2 tank
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x10])

    #Combo Meter Fuel 3/4 tank
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x20])

    #Combo Meter Fuel 4/4 tank
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x40])

    #Combo Meter Fuel Empty
    #ecom.send_iso_tp_data(0x7C0, [0x30, 0x03, 0x00, 0x80])

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
    while(1):
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
    #for i in range(0, 100):
    #    ecom.send_iso_tp_data(0x7E0, [0x30, 0x1C, 0x00, 0x0F, 0xA5, 0x01])
    #pkg = PriusCMD["Fuel_Cut_All"]
    #ecom.send_iso_tp_data(pkg['ID'], pkg['Data'])

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
