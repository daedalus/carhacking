from ctypes import *

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
handle = mydll.open_device(1,0)

def key_from_seed(seed):
    
#    print "Observed seed: "+seed
    #
    # This is the "secret" found in debugger
    #
    s1 = 0x08
    s2 = 0x30
    s3 = 0x61
    s4 = 0xa4
    s5 = 0xc5

    seed_int = (int(seed[0:2],16)<<16) + (int(seed[3:5],16)<<8) + (int(seed[6:8],16)) 
    or_ed_seed = ((seed_int & 0xFF0000) >> 16) | (seed_int & 0xFF00) | (s1 << 24) | (seed_int & 0xff) << 16
    mucked_value = 0xc541a9

    for i in range(0,32):
        a_bit = ((or_ed_seed >> i) & 1 ^ mucked_value & 1) << 23
        v9 = v10 = v8 = a_bit | (mucked_value >> 1);
        mucked_value = v10 & 0xEF6FD7 | ((((v9 & 0x100000) >> 20) ^ ((v8 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v8 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v8 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v8 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v8 & 0x800000) >> 23));

    for j in range(0,32):
        a_bit = ((((s5 << 24) | (s4 << 16) | s2 | (s3 << 8)) >> j) & 1 ^ mucked_value & 1) << 23;
        v14 = v13 = v12 = a_bit | (mucked_value >> 1);
	mucked_value = v14 & 0xEF6FD7 | ((((v13 & 0x100000) >> 20) ^ ((v12 & 0x800000) >> 23)) << 20) | (((((mucked_value >> 1) & 0x8000) >> 15) ^ ((v12 & 0x800000) >> 23)) << 15) | (((((mucked_value >> 1) & 0x1000) >> 12) ^ ((v12 & 0x800000) >> 23)) << 12) | 32 * ((((mucked_value >> 1) & 0x20) >> 5) ^ ((v12 & 0x800000) >> 23)) | 8 * ((((mucked_value >> 1) & 8) >> 3) ^ ((v12 & 0x800000) >> 23));

    key = ((mucked_value & 0xF0000) >> 16) | 16 * (mucked_value & 0xF) | ((((mucked_value & 0xF00000) >> 20) | ((mucked_value & 0xF000) >> 8)) << 8) | ((mucked_value & 0xFF0) >> 4 << 16);

#    print "Computed key: %x" % key
    return "%02X %02X %02X" % ( (key & 0xff0000) >> 16, (key & 0xff00) >> 8, key & 0xff) 


def send_to_e0(mydll, handle, line):
    yy = pointer(SFFMessage())
    mydll.DbgLineToSFF("IDH: 07, IDL: E0, Len: 08, Data: "+line, yy)
    mydll.PrintSFF(yy,0)
    mydll.write_message(handle, yy)
    read_by_wid = mydll.read_message_by_wid
    read_by_wid.restype = POINTER(SFFMessage)
    z = mydll.read_message_by_wid(handle, 0x7e8)
    mydll.PrintSFF(z,0)
    first_byte = z.contents.data[0]
    ret = ""

    if first_byte > 0x8:
        toread = ((first_byte & 0xf) << 8) + z.contents.data[1]
        toread -= 6
        ret = z.contents.data[2:]
        mydll.DbgLineToSFF("IDH: 07, IDL: E0, Len: 08, Data: 30 00 00 00 00 00 00 00", yy)
        mydll.PrintSFF(yy,0)
        mydll.write_message(handle, yy)
        while( toread > 0 ):
            z = mydll.read_message_by_wid(handle, 0x7e8)
            toread -= 7
            mydll.PrintSFF(z,0)
            ret += z.contents.data[1:]
    else:
        ret = z.contents.data[1:]
    strret = ""
    for x in ret:
        strret += "%02X " % x
    return strret


#raw_input("make sure car is in bootrom mode, use CarDaqPlusCat")
send_to_e0(mydll, handle, "02 10 02 00 00 00 00 00")
seed = send_to_e0(mydll, handle, "02 27 01 00 00 00 00 00")
#print seed
key = key_from_seed(seed[6:])
send_to_e0(mydll, handle, "05 27 02 "+key+" 00 00")
#send_to_e0(mydll, handle, "07 23 14 00 0f 80 00 10")
send_to_e0(mydll, handle, "07 23 14 00 01 00 C0 10")

mydll.close_device(handle)

