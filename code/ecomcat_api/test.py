from ctypes import *
import time

mydll = CDLL('Debug\\ecomcat_api')
#

class SFFMessage(Structure):
    _fields_ = [("IDH", c_ubyte),
                ("IDL", c_ubyte),
                ("data", c_ubyte * 8),
                ("options", c_ubyte),
                ("DataLength", c_ubyte),
                ("TimeStamp", c_uint),
                ("baud", c_ubyte)]


# initalize

# HS CAN
handle = mydll.open_device(1,37445)
#handle = mydll.open_device(1,37442)
# MS CAN
#handle = mydll.open_device(3,0)


#
# Turn on video camera (must not be in park)
#
#y = pointer(SFFMessage())
#mydll.DbgLineToSFF("IDH: 02, IDL: 30, Len: 08, Data: A1 00 00 00 00 00 5D 30", y)
#mydll.write_message_cont(handle, y, 1000)



#
# Make the pam beep with sensor stuff
#
y = pointer(SFFMessage())
mydll.DbgLineToSFF("IDH: 02, IDL: 30, Len: 08, Data: A1 00 00 00 00 00 3D 30", y)
#mydll.write_message_cont(handle, y, 20000)
#while True:
#    mydll.PrintSFF(y,0)
#    mydll.write_message(handle, y)
#    time.sleep(.01)



# read and print message from device
#z = mydll.read_message_by_wid(handle, 0x136)
#z = mydll.read_message(handle)
#mydll.PrintSFF(z,0)



# define and fill some messaegs
#x = SFFMessage()
#x.IDH = 0x69
#x.IDL = 0x41


#mydll.DbgLineToSFF("IDH: 07, IDL: 60, Len: 08, Data: 02 10 81 00 00 00 00 00", y)
#mydll.PrintSFF(y,0)
#mydll.write_message(handle, y)


# write single messages
#mydll.write_message(0, byref(x))
#mydll.write_message_cont(handle, y, 1000)

# create an array of messages
#SFFArray = SFFMessage * 10
#sffs = SFFArray()
#mydll.DbgLineToSFF("IDH: 01, IDL: 67, Len: 08, Data: 41 41 41 41 41 41 41 41", pointer(sffs[0]))
#mydll.DbgLineToSFF("IDH: 01, IDL: 68, Len: 08, Data: 42 42 42 42 42 42 42 42", pointer(sffs[1]))
#mydll.DbgLineToSFF("IDH: 01, IDL: 69, Len: 08, Data: 43 43 43 43 43 43 43 43", pointer(sffs[2]))
#print sffs[2].IDL

# write out some of the message stuffs
#mydll.write_messages_cont(handle, pointer(pointer(sffs)), 1000)


mydll.write_messages_from_file(handle, "long_reverse18.dat")

mydll.close_device(handle)
#mydll.PrintSFF(y, 0)

#print "%x" % x.IDH
#print "%x" % y.contents.IDL
#print "%x" % sffs[0].IDL
