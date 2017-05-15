from FordStuff import *
import sys

if len(sys.argv) < 3:
    sys.exit('Usage: %s rpm mph' % sys.argv[0])

rpm = int(sys.argv[1])
mph = int(sys.argv[2])

can_mph = int( 154 * (mph + 67) )
can_rpm = int( 4 * (rpm + 24) )

# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)

y = pointer(SFFMessage())
mydll.DbgLineToSFF("IDH: 02, IDL: 01, Len: 08, Data: %02X %02X 00 00 %02X %02X 00 00" % ((can_rpm & 0xff00) >> 8, can_rpm & 0xff, (can_mph & 0xff00) >> 8, can_mph & 0xff), y)
    
while True:
	mydll.write_message_cont(handle, y, 1000)

mydll.close_device(handle)
