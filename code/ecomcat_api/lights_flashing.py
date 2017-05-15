from FordStuff import *

# initalize
mydll = CDLL('Debug\\ecomcat_api')

# MS CAN
handle = mydll.open_device(3,0)
wid = 0x726
if do_diagnostic_session(mydll, handle, wid, "prog"):
	print "Started diagnostic session"
	time.sleep(1)
do_security_access(mydll, handle, wid)

if do_download(mydll, handle, wid, 0x0, '726_000000-again.firmware'):
	print do_proprietary(mydll, handle, wid, 0xb2, [0x01])
        # uncomment to fix lights
	#do_download(mydll, handle, wid, 0x7fc000, '726_007fc0-again.firmware')
        #send_data(mydll, handle, wid, [0x11,0x01])
	
send_data(mydll, handle, wid, [0x10, 0x81])

mydll.close_device(handle)
