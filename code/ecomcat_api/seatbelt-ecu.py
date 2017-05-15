from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,37440)
    #ecom.open_device(1,0)

    ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x01])

    time.sleep(3)
    
    ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x02])

    #read one message (should contain payload of: 0x08)
    #sff = pointer(SFFMessage())
    #ecom.mydll.DbgLineToSFF("IDH: 03, IDL: 44, Len: 08, Data: FF 7F 00 00 00 08 00 D5", sff)

    #ret = ecom.send_iso_tp_data(0x781, [0x3E])
    
    #ecom.mydll.write_messages_from_file(ecom.handle, "input.dat")
    #ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x01])

    #ret = ecom.mydll.read_message_by_wid(ecom.handle, 0x039C)
    #ecom.mydll.write_messages_from_file(ecom.handle, "car-startup-trim.dat")

    #ret = ecom.mydll.read_message_by_wid(ecom.handle, 0x039C)
    #ecom.mydll.write_messages_from_file(ecom.handle, "car-startup-trim.dat")    

    #read the messages from the wire
    #i = 0
    #while(i < 10):
    #    ret = ecom.mydll.read_message_by_wid(ecom.handle, 0x039C)
    #    ecom.mydll.PrintSFF(ret,0)
    #    i += 1

    #ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x01])
    #ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x02])

    #    for j in range(0, 20):
    #        ecom.mydll.write_message(ecom.handle, sff)
    #        time.sleep(.05)

        #ret = ecom.mydll.read_message_by_wid(ecom.handle, 0x04D4)
        #ecom.mydll.PrintSFF(ret,0)
        
        
        #ecom.diagnostic_session(0x781, [0x10, 0x01])
        #ecom.send_iso_tp_data(0x781, [0x30, 0x01, 0x00, 0x01])
    #    i += 1
