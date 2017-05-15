from FordStuff import *

# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
handle = mydll.open_device(1,0)

z = pointer(SFFMessage())
read_by_wid = mydll.read_message_by_wid_with_timeout
read_by_wid.restype = POINTER(SFFMessage)
z = read_by_wid(handle, 0x420)
mydll.PrintSFF(z,0)
odometer = z.contents.data[0] << 16
odometer += z.contents.data[1] << 8
odometer += z.contents.data[2]

yy = pointer(SFFMessage())

while True:
	odometer += 0x1000
	mydll.DbgLineToSFF("IDH: 04, IDL: 20, Len: 08, Data: %02x %02x %02x 00 00 00 02 00 ,TS: 17342,BAUD: 205" % ((odometer & 0xff0000) >> 16, (odometer & 0xff00) >> 8, odometer & 0xff), yy)
	mydll.PrintSFF(yy,0)
	mydll.write_message(handle, yy)

mydll.close_device(handle)
