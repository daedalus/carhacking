from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37440)

    brake_sff_str = "IDH: 02, IDL: 83, Len: 07, Data: 61 00 E0 BE 8C 00 17"
    brake_sff = SFFMessage()
    ecom.mydll.DbgLineToSFF(brake_sff_str, pointer(brake_sff))
    

    print "Starting to send msgs"
    while(1):
        brake_sff.data[0] += 1 & 0x7F
        ecom.mydll.FixChecksum(pointer(brake_sff))
        #ecom.mydll.PrintSFF(pointer(brake_sff), 0)
        ecom.mydll.write_message(ecom.handle, pointer(brake_sff))
        time.sleep(.001)
