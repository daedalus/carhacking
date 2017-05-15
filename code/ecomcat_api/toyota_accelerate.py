from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37436)

    #SFFLINE = "IDH: 00, IDL: 37, Len: 07, Data: C2 13 52 03 AC 00 14"
    #SFFLINE = "IDH: 00, IDL: 37, Len: 07, Data: C8 FE 58 13 E4 00 53"
    SFFLINE = "IDH: 00, IDL: 37, Len: 07, Data: C6 13 18 0E ED 00 2A"

    SFFArray = SFFMessage * 1
    SFFS = SFFArray()

    ecom.mydll.DbgLineToSFF(SFFLINE, pointer(SFFS[0]))

    ecom.mydll.FixChecksum(pointer(SFFS[0]))

    while(1):
        ecom.mydll.write_message(ecom.handle, pointer(SFFS[0]))
        #time.sleep(.0003)

    NOCHECK = 1

    while(1):

        #read_by_wid = ecom.mydll.read_message_by_wid_with_timeout
        #read_by_wid.restype = POINTER(SFFMessage)
        #sff_resp = ecom.mydll.read_message_by_wid_with_timeout(ecom.handle, 0x0037, 1000)

        #if(sff_resp[0].data[0] == 0xC2):
        #    SFFS[0] = sff_resp[0]
        #    break
    
        #increment two bytes
        X1 = SFFS[0].data[0]
        X2 = SFFS[0].data[1]
        if(X2 == 0xFF):
            if(X1 < 0xC9):
                X1 += 1

        #X2
        X2 += 1 & 0xFF

        SFFS[0].data[0] = X1
        SFFS[0].data[1] = X2
        
        for i in range(0, 2):
            Y1 = SFFS[0].data[3]
            Y2 = SFFS[0].data[4]
            if(Y2 == 0xFF):
                if(Y1 < 0xFF):
                    Y1 += 1

            #Y2
            Y2 += 1 & 0xFF

            SFFS[0].data[3] = Y1
            SFFS[0].data[4] = Y2            
            ecom.mydll.PrintSFF(pointer(SFFS[0]), 0)

            ecom.mydll.FixChecksum(pointer(SFFS[0]))
            
            ecom.mydll.write_message(ecom.handle, pointer(SFFS[0]))
            #time.sleep(.005)
