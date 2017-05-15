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

while True:
	send_data(mydll, handle, wid, [0x7e, 0x80])
	time.sleep(.1)

mydll.close_device(handle)
