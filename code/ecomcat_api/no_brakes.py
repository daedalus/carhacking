from FordStuff import *

# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)
wid = 0x760

while True:
    if not len( do_proprietary(mydll, handle, wid, 0x2b, [0xff, 0xff])):
        do_diagnostic_session(mydll, handle, wid, "adj")        

mydll.close_device(handle)
