from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37436)

    #f = open("can2-startup-min-drivers.dat", "r")
    f = open("can2-passenger.dat", "r")
    sff_lines = f.readlines()

    num_of_sffs =  len(sff_lines)
    SFFArray = SFFMessage * num_of_sffs
    sffs = SFFArray()

    for i in range(0, num_of_sffs):
        ecom.mydll.DbgLineToSFF(sff_lines[i], pointer(sffs[i]))

    print "Starting to send msgs"
    
    #ecom.mydll.write_messages_from_file(ecom.handle, "input.dat")
    #ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x01])

    while(1):
##        for i in range(0, 30):
##            ecom.mydll.write_message(ecom.handle, sff_0024_F9)
##
##        for i in range(0, 4):
##            ecom.mydll.write_message(ecom.handle, sff_0344)
##
##        for i in range(0, 4):
##            ecom.mydll.write_message(ecom.handle, sff_0024_F8)
            
        #ecom.mydll.write_message(ecom.handle, sff_0024)
        #ecom.mydll.write_message(ecom.handle, sff_0024)
        #ecom.mydll.write_message(ecom.handle, sff_0344)
        #time.sleep(.01)
        
        for i in range(0, num_of_sffs):
            ecom.mydll.write_message(ecom.handle, pointer(sffs[i]))
        #for j in range(0, 20):
        #    #ecom.mydll.write_message(ecom.handle, sff)
        #    ecom.mydll.write_messages_from_file(ecom.handle, "can2-startup-piece.dat")
        #    #time.sleep(.05)
