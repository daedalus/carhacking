from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37440)

    LOOPER = 0
    SETSPEED = 62
    SFFLINE = "IDH: 07, IDL: C0, Len: 08, Data: 04 30 01 00 02 00 00 00"

    SFFArray = SFFMessage * 1
    SFFS = SFFArray()

    ecom.mydll.DbgLineToSFF(SFFLINE, pointer(SFFS[0]))

    #if(SETSPEED < 200):
    #    SETSPEED = SETSPEED * 161

    #SFFS[0].data[0] = (SETSPEED >> 8) & 0xFF; 
    #SFFS[0].data[1] = SETSPEED & 0xFF;

    #ecom.mydll.FixChecksum(pointer(SFFS[0]))

    while(1):
        ecom.send_iso_tp_data(0x7C0, [0x30, 0x01, 0x00, 0x08])
