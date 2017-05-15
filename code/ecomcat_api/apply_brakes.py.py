from FordStuff import *

# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)
wid = 0x760

if do_diagnostic_session(mydll, handle, wid, "adj"):
    print "Started diagnostic session"

while True:
    print do_proprietary(mydll, handle, wid, 0x3c, [0x7f]) 

mydll.close_device(handle)
