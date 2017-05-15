from FordStuff import *

# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)
wid = 0x736

filename = 'try_send_can.bin'

if do_diagnostic_session(mydll, handle, wid, "prog"):
	print "Started diagnostic session"
	time.sleep(1)
do_security_access(mydll, handle, wid)

try:
   with open(filename): pass
except IOError:
   print 'Need firmware file to upload'
   sys.exit(0)

if do_download_compliant(mydll, handle, wid, 0x0, filename):
	do_routine(mydll, handle, wid, 0x0301, [0x00, 0x00, 0x30, 0x00])

mydll.close_device(handle)
