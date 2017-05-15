from FordStuff import *
import time


# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)


# get current
read_by_wid = mydll.read_message_by_wid_with_timeout
read_by_wid.restype = POINTER(SFFMessage)
z = mydll.read_message_by_wid_with_timeout(handle, 0x80, 1000)
current = (z.contents.data[0]<<8) + z.contents.data[1]
print "Current wheel at %x" % current
change = 0
y = pointer(SFFMessage())

while(True):
	current += change
	change += 12
	mydll.DbgLineToSFF("IDH: 00, IDL: 81, Len: 08, Data: %02X %02X 12 00 00 00 00 00" % ((current & 0xff00) >> 8, current & 0xff), y)
	mydll.write_message_cont(handle, y)	
	time.sleep(.0019)  # should be 312 ticks

mydll.close_device(handle)
