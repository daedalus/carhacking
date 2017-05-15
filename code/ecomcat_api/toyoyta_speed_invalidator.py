from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37440)

    LOOPER = 0

    f = open("speed_bad.dat", "r")
    sff_lines = f.readlines()

    num_of_sffs =  len(sff_lines)
    SFFArray = SFFMessage * num_of_sffs
    sffs = SFFArray()

    for i in range(0, num_of_sffs):
        ecom.mydll.DbgLineToSFF(sff_lines[i], pointer(sffs[i]))

    print "Starting to send msgs"
    while(1):
        for i in range(0, num_of_sffs):
            curr = sffs[i]

##            if LOOPER == 1:
##                #if curr.IDH == 0x00 and curr.IDL == 0xB4:
##                #    curr.data[4] += 1 & 0xFF
##                if curr.IDH == 0x02 and curr.IDL == 0xE4:
##                    curr.data[0] += 1 & 0xFF
##                    curr.data[0] |= 0x80
##                if curr.IDH == 0x02 and curr.IDL == 0x83:
##                    curr.data[0] += 1 & 0x7F
##
##                ecom.mydll.FixChecksum(pointer(curr))
                
            #ecom.mydll.PrintSFF(pointer(curr), 0)
            ecom.mydll.write_message(ecom.handle, pointer(curr))
