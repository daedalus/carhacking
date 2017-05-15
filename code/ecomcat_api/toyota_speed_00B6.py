from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37440)

    LOOPER = 0
    SETSPEED = 62
    SFFLINE = "IDH: 00, IDL: B6, Len: 04, Data: 00 00 00 BA"

    SFFArray = SFFMessage * 1
    SFFS = SFFArray()

    ecom.mydll.DbgLineToSFF(SFFLINE, pointer(SFFS[0]))

    if(SETSPEED < 200):
        SETSPEED = SETSPEED * 161

    SFFS[0].data[0] = (SETSPEED >> 8) & 0xFF; 
    SFFS[0].data[1] = SETSPEED & 0xFF;

    ecom.mydll.FixChecksum(pointer(SFFS[0]))

    while(1):
        #ecom.mydll.PrintSFF(pointer(SFFS[0]), 0)
        ecom.mydll.write_message(ecom.handle, pointer(SFFS[0]))
