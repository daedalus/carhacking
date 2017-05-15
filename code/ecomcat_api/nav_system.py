from FordStuff import *

# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)

z = pointer(SFFMessage())
read_by_wid = mydll.read_message_by_wid_with_timeout
read_by_wid.restype = POINTER(SFFMessage)
z = read_by_wid(handle, 0x217)
mydll.PrintSFF(z,0)
wheel = z.contents.data[0] << 8
wheel += z.contents.data[1]

print "%x" % wheel
yy = pointer(SFFMessage())

while True:
    wheel += 0x1
    mydll.DbgLineToSFF("IDH: 02, IDL: 17, Len: 08, Data: %02x %02x %02x %02x 00 50 00 00 ,TS: 17342,BAUD: 205" % ((wheel & 0xff00) >> 8, wheel & 0xff, (wheel & 0xff00) >> 8, wheel & 0xff), yy)
    mydll.PrintSFF(yy,0)
    mydll.write_message(handle, yy)
