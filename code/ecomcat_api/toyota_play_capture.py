from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,35916)

    LOOPER = 0

    f = open("regular.dat", "r")
    sff_lines = f.readlines()

    num_of_sffs =  len(sff_lines)
    SFFArray = SFFMessage * num_of_sffs
    sffs = SFFArray()

    for i in range(0, num_of_sffs):
        ecom.mydll.DbgLineToSFF(sff_lines[i], pointer(sffs[i]))

    print "Starting to send wheel msgs"
    while(1):
        for i in range(0, num_of_sffs):
            ecom.mydll.write_message(ecom.handle, pointer(sffs[i]))
