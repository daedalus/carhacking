from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37440)

    #Changed data[3] (0x80) to 0x40 if you want beeping
    SFFLINE = "IDH: 02, IDL: E4, Len: 05, Data: 80 05 00 80 F0"

    SFFArray = SFFMessage * 1
    SFFS = SFFArray()

    ecom.mydll.DbgLineToSFF(SFFLINE, pointer(SFFS[0]))

    while(1):
        SFFS[0].data[0] += 1 & 0xFF; 
        SFFS[0].data[0] |= 0x80;
        ecom.mydll.FixChecksum(pointer(SFFS[0]))
        
        #ecom.mydll.PrintSFF(pointer(SFFS[0]), 0)
        ecom.mydll.write_message(ecom.handle, pointer(SFFS[0]))
