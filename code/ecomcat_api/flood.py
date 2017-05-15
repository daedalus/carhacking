from FordStuff import *
import sys

if len(sys.argv) < 2:
    sys.exit('Usage: %s serialnum' % sys.argv[0])

# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1, int(sys.argv[1]))

y = pointer(SFFMessage())
mydll.DbgLineToSFF("IDH: 00, IDL: 00, Len: 08, Data: 00 00 00 00 00 00 00 00", y)

while True:
	mydll.write_message_cont(handle, y, 1000)

mydll.close_device(handle)
