from ctypes import *
import time
import struct

class SFFMessage(Structure):
    _fields_ = [("IDH", c_ubyte),
                ("IDL", c_ubyte),
                ("data", c_ubyte * 8),
                ("options", c_ubyte),
                ("DataLength", c_ubyte),
                ("TimeStamp", c_uint),
                ("baud", c_ubyte)]

secret_keys = {
                0x726: "3F 9E 78 C5 96",
		0x727: "50 C8 6A 49 F1",
		0x733: "AA BB CC DD EE",
		0x736: "08 30 61 55 AA",
		0x737: "52 6F 77 61 6E",
		0x760: "5B 41 74 65 7D",
		0x765: "96 A2 3B 83 9B",
		0x7a6: "50 C8 6A 49 F1",
		0x7e0: "08 30 61 A4 C5",}

secret_keys2 = {
                0x7e0: "44 49 4F 44 45",
                0x737: "5A 89 E4 41 72"}

def key_from_seed(wid, seed, mode):

    secret = ""
    if mode == 1:
        if not secret_keys.has_key(wid):
            return [0,0,0]
 
        secret = secret_keys[wid]
    else:
        if not secret_keys2.has_key(wid):
            return [0,0,0]
        secret = secret_keys2[wid]
        
    s1 = int(secret[0:2],16)
    s2 = int(secret[3:5],16)
    s3 = int(secret[6:8],16)
    s4 = int(secret[9:11],16)
    s5 = int(secret[12:14],16)

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
#    return "%02X %02X %02X" % ( (key & 0xff0000) >> 16, (key & 0xff00) >> 8, key & 0xff) 
    return [(key & 0xff0000) >> 16, (key & 0xff00) >> 8, key & 0xff]

def do_routine(mydll, handle, wid, routineIdentifier, options):

    	rlow = routineIdentifier & 0xff
    	rhigh = (routineIdentifier & 0xff00) >> 8
    	yy = pointer(SFFMessage())
        data = [0x31,1,rhigh,rlow] + options
	resp = send_data(mydll, handle, wid, data)
        print "[%02X] Calling routine %04X: " % (wid, routineIdentifier),
        if not resp:
                print "No response"
                return
        if resp[0] == 0x71:
                print "Worked"
                return
	if resp[1] != 0x31:
		print "Weird, got wrong response"
            	return
	if resp[0] == 0x7f:
            	print "Failed, error code %02X" % resp[2]
        else:
            	print "worked, got %02X" % resp[2]


def do_routine_14230_by_address(mydll, handle, wid, address, options):
	address1 = (address & 0xff0000) >> 16
	address2 = (address & 0xff00) >> 8
	address3 = (address & 0xff)

        data = [0x38,address1,address2,address3] + options
	resp = send_data(mydll, handle, wid, data)
        print "[%02X] Calling routine %X: " % (wid, address),
        if not resp:
                print "No response"
                return
        if resp[0] == 0x78:
                print "Worked"
                return
	if resp[1] != 0x38:
		print "Weird, got wrong response"
            	return
	if resp[0] == 0x7f:
            	print "Failed, error code %02X" % resp[2]
        else:
            	print "worked, got %02X" % resp[2]


def do_routine_14230(mydll, handle, wid, routineIdentifier, options):
        data = [0x31,routineIdentifier] + options
	resp = send_data(mydll, handle, wid, data)
        print "[%02X] Calling routine %04X: " % (wid, routineIdentifier),
        if not resp:
                print "No response"
                return
        if resp[0] == 0x71:
                print "Worked"
                return
	if resp[1] != 0x31:
		print "Weird, got wrong response"
            	return
	if resp[0] == 0x7f:
            	print "Failed, error code %02X" % resp[2]
        else:
            	print "worked, got %02X" % resp[2]


def do_routine_14230_get_response(mydll, handle, wid, routineIdentifier, options):
        data = [0x31,routineIdentifier] + options
	resp = send_data(mydll, handle, wid, data)
        print "[%02X] Calling routine %04X: " % (wid, routineIdentifier),
        if not resp:
                print "No response"
                return []
        if resp[0] == 0x71:
                print "Worked"
	elif resp[1] != 0x31:
		print "Weird, got wrong response"
            	return []
	elif resp[0] == 0x7f:
            	print "Failed, error code %02X" % resp[2]
            	return []
        ret = []
        while len(ret) == 0:
            resp = send_data(mydll, handle, wid, [0x33, routineIdentifier])
            if resp[0] == 0x7f and resp[1] == 0x33 and resp[2] == 0x21:
                print "."
            elif resp[0] == 0x73:
                print "worked 2"
#                print resp
                return resp[2:]
            else:
                print "?"
            time.sleep(.1)
        


def data_to_line(data, linelen):
	line = ''
	x = 0
	while x < len(data):
		line += "%02X " % data[x]
		x += 1

	while x < linelen:
		line += "00 "
		x += 1

	return line


#
# This function sends data using ISO TP and reads the response using ISO TP
#
def send_data(mydll, handle, wid, data):
	yy = pointer(SFFMessage())
	idh = (wid & 0xff00) >> 8
	idl = (wid & 0xff)

	# multi packet send
	if len(data) > 7:
#                print "Long data"
		# first packet
		datalen = len(data)

                # CV fix for payloads over 0xFF bytes in length
                #datalen = datalen & 0x0FFF
                #data_bytes = (0x01000 | datalen) & 0x0FFFF
                #byteone = (data_bytes >> 8)
                #bytetwo = data_bytes & 0xFF
		
		byteone = 0x10 + (0xf00 & datalen)
		bytetwo = 0xff & datalen
		firstdata = [byteone, bytetwo] + data[0:6]
		line = "IDH: %02X, IDL: %02X, Len: 08, Data: " % (idh, idl)
                line += data_to_line(firstdata, 8)
                mydll.DbgLineToSFF(line, yy)
                mydll.PrintSFF(yy,0)
                mydll.write_message(handle, yy)
		# resp
                read_by_wid = mydll.read_message_by_wid_with_timeout
                read_by_wid.restype = POINTER(SFFMessage)
        	z = mydll.read_message_by_wid_with_timeout(handle, wid+8, 1000)
		sent = 6
		counter = 0
        	mydll.PrintSFF(z,0)
		if z.contents.data[0] != 0x30:
			print "Bad response"
			return []

		# rest
		while sent < datalen:
			firstbyte = 0x20 + ((counter+1) & 0xf)
			firstdata = [firstbyte] + data[6 + counter*7 : 13 + counter*7]
			line = "IDH: %02X, IDL: %02X, Len: 08, Data: " % (idh, idl)
                	line += data_to_line(firstdata, 8)
                	mydll.DbgLineToSFF(line, yy)
                	mydll.PrintSFF(yy,0)
                	mydll.write_message(handle, yy)
			sent += 7
			counter += 1
	else:
		# single packet send
		line = "IDH: %02X, IDL: %02X, Len: 08, Data: %02x " % (idh, idl, len(data))
		line += data_to_line(data, 8) 
		mydll.DbgLineToSFF(line, yy)
		mydll.PrintSFF(yy,0)
    		mydll.write_message(handle, yy)


	# get response
    	read_by_wid = mydll.read_message_by_wid_with_timeout
    	read_by_wid.restype = POINTER(SFFMessage)
    	z = mydll.read_message_by_wid_with_timeout(handle, wid+8, 1000)
    	
	if not z:
		return []

        mydll.PrintSFF(z,0)
    	first_byte = z.contents.data[0]

    	if first_byte < 0x8:
            # is it a slow operation?
            while z.contents.data[1] == 0x7f and z.contents.data[3] == 0x78:
                time.sleep(.1)
                z = mydll.read_message_by_wid_with_timeout(handle, wid+8, 1000)
                if not z:
                    return []
                mydll.PrintSFF(z,0)
	    return z.contents.data[1:]

	toread = ((first_byte & 0xf) << 8) + z.contents.data[1]
	total_to_read = toread
        toread -= 6
	ret = z.contents.data[2:]
        mydll.DbgLineToSFF("IDH: %02X, IDL: %02X, Len: 08, Data: 30 00 00 00 00 00 00 00" % (idh, idl), yy)
        mydll.PrintSFF(yy,0)
        mydll.write_message(handle, yy)
        while( toread > 0 ):
            	z = mydll.read_message_by_wid_with_timeout(handle, wid+8, 1000)
            	toread -= 7
		ret += z.contents.data[1:]
            	mydll.PrintSFF(z,0)
    	return ret[:total_to_read]

def try_ids(mydll, handle, wid):
    for x in range(0,255):
        print "Trying %02X:" % x,
        ret = send_data(mydll, handle, wid, [x])
        while len(ret) == 0 or ret[2] == 0x21:
            ret = send_data(mydll, handle, wid, [0x10,x])
        if ret[2] != 0x11:
            print "Yes %x" % ret[2]
        else:
            print "No %x" % ret[2]

 
# the final line needs to be changed for 14230 to 81...
def try_all_diagnostic_sessions(mydll, handle, wid):
    for x in range(0,255):
        print "Trying %02X:" % x,
        ret = send_data(mydll, handle, wid, [0x10,x])
        while len(ret) == 0 or ret[2] == 0x21:
            ret = send_data(mydll, handle, wid, [0x10,x])
        if ret[0] == 0x50:
            print "Yes"
        else:
            print "No"
        send_data(mydll, handle, wid, [0x10, 0x1])

def do_diagnostic_session(mydll, handle, wid, session_type):
    tn_byte = 0x01
    t_byte = 0x81
    if session_type == "prog":
        tn_byte = 2
	t_byte = 0x85
    elif session_type == "adj":
	tn_byte = 3
	t_byte = 0x87
    elif session_type == "prop":
        tn_byte = 4
        t_byte = 0xf0

    ret = send_data(mydll, handle, wid, [0x10, tn_byte])
    if not ret:
        print "No response"
        return False
    if ret[0] == 0x50:
        return True
    # try 80 one:
    ret = send_data(mydll, handle, wid, [0x10, t_byte])
    if not ret:
        print "No response"
        return False
    if ret[0] == 0x50:
        return True
    if ret[2] == 0x78:
    	read_by_wid = mydll.read_message_by_wid_with_timeout
    	read_by_wid.restype = POINTER(SFFMessage)
    	z = mydll.read_message_by_wid_with_timeout(handle, wid+8, 1000)
        mydll.PrintSFF(z,0)
        if z.contents.data[1] == 0x50:
            return True
    print "Couldn't start diagnostic session"
    return False



def do_security_access2(mydll, handle, wid):
    seed = send_data(mydll, handle, wid, [0x27,3])
    if not seed:
        print "no response"
        return
    strseed = ''
    for x in seed:
        strseed += "%02X " % x
#    print seed
    key = key_from_seed(wid, strseed[6:], 2)
    send_data(mydll, handle, wid, [0x27,4]+key)


def do_security_access(mydll, handle, wid):
    seed = send_data(mydll, handle, wid, [0x27,1])
    if not seed:
        print "no response"
        return
    strseed = ''
    for x in seed:
        strseed += "%02X " % x
#    print seed
    key = key_from_seed(wid, strseed[6:], 1)
    ret = send_data(mydll, handle, wid, [0x27,2]+key)
    if ret[0] == 0x67:
	print "Got access"
    else:
	print "Denied!"



def do_write_memory(mydll, handle, wid, address, d):
    size = len(d)
    data = []
    address1 = (address & 0xff000000) >> 24
    address2 = (address & 0xff0000) >> 16
    address3 = (address & 0xff00) >> 8
    address4 = (address & 0xff)
    if size < 0xff:    
        data = [0x3d, 0x14, address1, address2, address3, address4, size]+d
    else:
        size1 = (size & 0xff000000) >> 24
        size2 = (size & 0xff0000) >> 16
        size3 = (size & 0xff00) >> 8
        size4 = (size & 0xff)
        data = [0x3d, 0x44, address1, address2, address3, address4, size1, size2, size3, size4]+d
    resp = send_data(mydll, handle, wid, data)
    if resp[0] == 0x7d:
        return resp        
    if resp[1] != 0x3d:
        print "Weird response"
        return []
    print "Failed to write memory, error %x" % resp[2]
    return resp

#
# not really 14430 - but ford-14430 from dll
#
def do_read_memory_14430(mydll, handle, wid, address, size):
        address1 = (address & 0xff000000) >> 24
        address2 = (address & 0xff0000) >> 16
        address3 = (address & 0xff00) >> 8
        address4 = (address & 0xff)

        size1 = (size & 0xff00) >> 8
        size2 = (size & 0xff)

	resp = send_data(mydll, handle, wid, [0x23, address1, address2, address3, address4, size1, size2])
	if resp[0] == 0x63:
                print "OMG, it worked"
		return resp[1:]
	if resp[1] != 0x23:
		print "Weird response"
		return []
	print "Failed to read memory, error %x" % resp[2]
	return resp

def do_read_memory(mydll, handle, wid, address, size):
    data = []
    address1 = (address & 0xff000000) >> 24
    address2 = (address & 0xff0000) >> 16
    address3 = (address & 0xff00) >> 8
    address4 = (address & 0xff)
#    if size <= 0xff:
#        data = [0x23, 0x14, address1, address2, address3, address4, size]
#    else:
    size1 = (size & 0xff000000) >> 24
    size2 = (size & 0xff0000) >> 16
    size3 = (size & 0xff00) >> 8
    size4 = (size & 0xff)
    data = [0x23, 0x44, address1, address2, address3, address4, size1, size2, size3, size4]

    resp = send_data(mydll, handle, wid, data)
    if resp[0] == 0x63:
        return resp[1:]
    if resp[1] != 0x23:
        print "Weird response"
        return []
    print "Failed to read memory, error %x" % resp[2]
    return resp

def do_inputoutput(mydll, handle, wid, inputoutputID, options):
    	rlow = inputoutputID & 0xff
    	rhigh = (inputoutputID & 0xff00) >> 8
    	yy = pointer(SFFMessage())
        data = [0x2f,rhigh,rlow] + options
	resp = send_data(mydll, handle, wid, data)
        print "[%02X] Calling IO %04X: " % (wid, inputoutputID),
        if not resp:
                print "No response"
                return False
	if resp[0] == 0x7f:
            	print "Failed, error code %02X" % resp[2]
            	return False
        else:
            	print "worked, got %02X" % resp[2]
                return True

def do_inputoutput_14230(mydll, handle, wid, inputoutputID, options):
    	id1 = inputoutputID & 0xff

    	yy = pointer(SFFMessage())
        data = [0x30,id1] + options
	resp = send_data(mydll, handle, wid, data)
        print "[%02X] Calling IO %02X: " % (wid, id1),
        if not resp:
                print "No response"
                return False
	if resp[0] == 0x7f:
            	print "Failed, error code %02X" % resp[2]
            	return False
        else:
            	print "worked, got %02X" % resp[2]
                return True


def search_for_readable_memory(mydll, handle, wid):
    x = 0x0
    while x < 0xffff00:
        print "Reading from %x" % x,
        print do_read_memory(mydll, handle, wid, x, 0x10)
        x += 0x100


def search_for_pullable_memory(mydll, handle, wid):
    x = 0x0
    while x < 0xffff00:
        print "Reading from %x" % x
        ret = pull_data(mydll, handle, wid, x, 0x10)
        if len(ret)>0:
            print "Yes from %x" % x
        else:
            print "No from %x" % x
        x += 0x100
        # RequestTransferExit
        send_data(mydll, handle, wid, [0x37])



def pull_data_14230(mydll, handle, wid, address, size):
	data = []
        address1 = (address & 0xff000000) >> 24
        address2 = (address & 0xff0000) >> 16
        address3 = (address & 0xff00) >> 8
        address4 = (address & 0xff)

    	size1 = (size & 0xff0000) >> 16
    	size2 = (size & 0xff00) >> 8
    	size3 = (size & 0xff) 

        # guessing on the ol 01 flag
    	data = [0x35, address1, address2, address3, address4, 0x01, size1, size2, size3]

	#RequestUpload
	resp = send_data(mydll, handle, wid, data)
	
	# check for error codes
	if resp[0] != 0x75:
		print "Bad response"
		print resp
		return []
	
	resp = send_data(mydll, handle, wid, [0x36, 0x01])
	if resp[0] == 0x76:
		print "omg it worked"
		return resp[1:]
	print "error!"
	return []


def pull_data(mydll, handle, wid, address, size):
	data = []
	address1 = (address & 0xff000000) >> 24
	address2 = (address & 0xff0000) >> 16
	address3 = (address & 0xff00) >> 8
	address4 = (address & 0xff)
#
#	7e0 only likes 4 byte size requests
#
#	if size <= 0xff:
#		data = [0x35, 0x00, 0x14, address1, address2, address3, address4, size]
#	else:
    	size1 = (size & 0xff000000) >> 24
    	size2 = (size & 0xff0000) >> 16
    	size3 = (size & 0xff00) >> 8
    	size4 = (size & 0xff)
    	data = [0x35, 0x00, 0x44, address1, address2, address3, address4, size1, size2, size3, size4]

	#RequestUpload
	resp = send_data(mydll, handle, wid, data)
	
	# check for error codes
	if resp[0] != 0x75:
		print "Bad response"
		print resp
		return []
	
	resp = send_data(mydll, handle, wid, [0x36, 0x01])
	if resp[0] == 0x76:
		print "omg it worked"
		return resp[1:]
	print "error!"
	return []


def do_proprietary(mydll, handle, wid, did, options):
	data = []
	did1 = (did & 0xff00) >> 8
	did2 = (did & 0xff)

    	data = [0xb1, did1, did2] + options
    	
	resp = send_data(mydll, handle, wid, data)
	
	# check for error codes
	if resp[0] != 0xf1:
		print "Bad response"
		print resp
		return []
	print "worked %04X with len %d" % (did, len(options))
	return resp[1:]



# returns if it was able to get a valid response
def try_key(mydll, handle, wid, key):
	key1 = (key & 0xff0000) >> 16
	key2 = (key & 0xff00) >> 8
	key3 = (key & 0xff)

	ret = send_data(mydll, handle, wid, [0x27,2,key1,key2,key3])
	return ret

# need to loop
def brute_force_key(mydll, handle, wid):
	tries = {}
	key = 0

        while True:
	
            seed = []
            while len(seed) == 0:
                send_data(mydll, handle, wid, [0x11, 0x01])
                seed = send_data(mydll, handle, wid, [0x27,1])[2:5]
            print seed
            seed = (seed[0] << 16) + (seed[1]<<8) + (seed[2])
            print "Got seed %x" % seed
            if not tries.has_key(seed):
		tries[seed] = 0

            key = tries[seed]

            ret = try_key(mydll, handle, wid, key)
            if not ret:
		print "No repsonse"
            elif ret[0] == 0x67:
		print "Found it: %x %x" % (seed, key)
		return
            elif ret[0] == 0x7f and ret[1] == 0x27:
		print "Not it for %x %x, error %x" % (seed, key, ret[2])
		tries[seed] = key + 1	
            else:
		print "Weird response"

            print tries


def test_ecu(mydll, handle, wid):
	# do tests with normal session
#	print "Normal session"
#	do_security_access(mydll, handle, wid)
#	for id in [0,0x80,0x1000,0x8000]:
#		do_inputoutput(mydll, handle, wid, id, [])
#	for id in [0,0x8,0x10,0x80,0xff]:
#		do_inputoutput_14230(mydll, handle, wid, id, [])

	# do tests with programming session
        time.sleep(1)
	print "Programming"
    	do_diagnostic_session(mydll, handle, wid, "normal")
    	time.sleep(1)
	if do_diagnostic_session(mydll, handle, wid, "prog"):
		print "Started diagnostic session"
        time.sleep(1)
	do_security_access(mydll, handle, wid)

	for addy in [0,0x10,0x100,0x1000,0x10000,0x100000,0x1000000,0x10000000]:
		do_read_memory(mydll, handle, wid, addy, 0x10)
	for addy in [0,0x10,0x100,0x1000,0x10000,0x100000]:
		do_read_memory_14430(mydll, handle, wid, addy, 0x10)

        for addy in [0,0x10,0x100,0x1000,0x10000,0x100000,0x1000000,0x10000000]:
		pull_data(mydll, handle, wid, addy, 0x10)
        for addy in [0,0x10,0x100,0x1000,0x10000,0x100000]:
		pull_data_14230(mydll, handle, wid, addy, 0x10)

	for routine in [0,0x10, 0x80, 0x100, 0x800, 0x1000, 0x8000]:
		do_routine(mydll, handle, wid , routine, [])
	for routine in [0,0x10,0x100,0x1000,0x10000,0x100000]:
		do_routine_14230_by_address(mydll, handle, wid, routine, [])
	for routine in [0,0x8,0x10,0x80,0xff]:
		do_routine_14230(mydll, handle, wid, routine, [])

	do_security_access2(mydll, handle, wid)


	print "Adjustment"
	do_diagnostic_session(mydll, handle, wid, "normal")
        time.sleep(5)
        if do_diagnostic_session(mydll, handle, wid, "adj"):
                print "Started diagnostic session"
        do_security_access2(mydll, handle, wid)

        for addy in [0,0x10,0x100,0x1000,0x10000,0x100000,0x1000000,0x10000000]:
                do_read_memory(mydll, handle, wid, addy, 0x10)
        for addy in [0,0x10,0x100,0x1000,0x10000,0x100000]:
                do_read_memory_14430(mydll, handle, wid, addy, 0x10)

        for addy in [0,0x10,0x100,0x1000,0x10000,0x100000,0x1000000,0x10000000]:
                pull_data(mydll, handle, wid, addy, 0x10)
        for addy in [0,0x10,0x100,0x1000,0x10000,0x100000]:
                pull_data_14230(mydll, handle, wid, addy, 0x10)

        for routine in [0,0x10, 0x80, 0x100, 0x800, 0x1000, 0x8000]:
                do_routine(mydll, handle, wid, routine, [])
        for routine in [0,0x10,0x100,0x1000,0x10000,0x100000]:
                do_routine_14230_by_address(mydll, handle, wid, routine, [])
        for routine in [0,0x8,0x10,0x80,0xff]:
                do_routine_14230(mydll, handle, wid, routine, [])

        do_security_access2(mydll, handle, wid)

def kill_engine(mydll, handle, time):
    y = pointer(SFFMessage())
    mydll.DbgLineToSFF("IDH: 07, IDL: E0, Len: 08, Data: 05 31 01 40 44 FF 00 00", y)
    mydll.write_message_cont(handle, y, time)

def listify(thestring):
    l = list(thestring)
    ret = []
    for x in l:
        ret += [struct.unpack('B', x)[0]]
    return ret

def do_download_compliant(mydll, handle, wid, address, filename):
        address1 = (address & 0xff000000) >> 24
        address2 = (address & 0xff0000) >> 16
        address3 = (address & 0xff00) >> 8
        address4 = (address & 0xff)

        f = open(filename, 'rb')
        filedata = f.read()
        size = len(filedata)
	size1 = (size & 0xff000000) >> 24
        size2 = (size & 0xff0000) >> 16
        size3 = (size & 0xff00) >> 8
        size4 = (size & 0xff)

        data = [0x34, 0x0, 0x44, address1, address2, address3, address4, size1, size2, size3, size4]
        resp = send_data(mydll, handle, wid, data)

        if resp[0] != 0x74:
                print "Bad response to request download"
                print resp
                return False

        packetsize = resp[3]
        print "worked with packetsize %d" % packetsize

        cur = 0
        print "size is %d" % size
	packetnum = 1
        while cur + packetsize < size:
                print "Sending bytes from %d" % cur
                data = [0x36, packetnum] + listify(filedata[cur:cur+packetsize-2])
                resp = send_data(mydll, handle, wid, data)
                if resp[0] != 0x76:
                        print "Bad response to data transfer"
                        print resp
                        return False
                cur += packetsize - 2
		packetnum += 1

        print "sending end"
        data = [0x36, packetnum] + listify(filedata[cur:])
        resp = send_data(mydll, handle, wid, data)
        if resp[0] != 0x76:
                print "Bad response to data transfer"
                print resp
                return False

        resp = send_data(mydll, handle, wid, [0x37])

        if resp[0] != 0x77:
                print "Bad response to data exit"
                print resp
                return False

        print "Looks good!"
        return True




def do_download(mydll, handle, wid, address, filename):
	address1 = (address & 0xff000000) >> 24
	address2 = (address & 0xff0000) >> 16
	address3 = (address & 0xff00) >> 8
	address4 = (address & 0xff)

	f = open(filename, 'rb')
	filedata = f.read()
	size = len(filedata)
	size1 = (size & 0xff0000) >> 16
        size2 = (size & 0xff00) >> 8
        size3 = (size & 0xff)

#	data = [0x34, addy1, addy2, addy3, 0, 1, size1, size2, size3]
        data = [0x34, address1, address2, address3, address4, 1, size1, size2, size3]
	resp = send_data(mydll, handle, wid, data)
        
	if resp[0] != 0x74:
                print "Bad response to request download"
                print resp
                return False

	packetsize = resp[2]
        print "worked with packetsize %d" % packetsize
	
	cur = 0
	print "size is %d" % size
	while cur + packetsize < size:
                print "Sending bytes from %d" % cur
		data = [0x36] + listify(filedata[cur:cur+packetsize-1])
		resp = send_data(mydll, handle, wid, data)
        	if resp[0] != 0x76:
                	print "Bad response to data transfer"
                	print resp
                	return False
		cur += packetsize - 1

        print "sending end"
	data = [0x36] + listify(filedata[cur:])
        resp = send_data(mydll, handle, wid, data)
        if resp[0] != 0x76:
        	print "Bad response to data transfer"
       		print resp
        	return False

	resp = send_data(mydll, handle, wid, [0x37])

        if resp[0] != 0x77:
                print "Bad response to data exit"
                print resp
                return False

        print "Looks good!"
	return True


# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
#handle = mydll.open_device(1,37445)
#handle = mydll.open_device(1,0)
#handle = mydll.open_device(1, 500744)

# MS CAN
handle = mydll.open_device(3,0)

#PAM
#wid = 0x736
#ABS
#wid = 0x760

#SJB
wid = 0x726

#		0x736: "08 30 61 55 AA",
#		0x737: "52 6F 77 61 6E",
#		0x760: "5B 41 74 65 7D",
#		0x765: "96 A2 3B 83 9B",
#		0x7e0: "08 30 61 A4 C5",}

#raw_input("make sure car is in bootrom mode, use CarDaqPlusCat")

#try_all_diagnostic_sessions(mydll, handle, wid)

# speedometer
#mydll.DbgLineToSFF("IDH: 02, IDL: 01, Len: 08, Data: 23 45 00 00 34 56 00 00 ,TS: 17342,BAUD: 205", yy)
# camera
#    mydll.DbgLineToSFF("IDH: 02, IDL: 30, Len: 08, Data: A1 00 00 00 00 00 64 30 ,TS: 17342,BAUD: 205", yy)
#mydll.DbgLineToSFF("IDH: 02, IDL: 17, Len: 08, Data: 20 00 20 00 00 00 00 00 ,TS: 17342,BAUD: 205", yy)
#mydll.PrintSFF(yy,0)

#while True:
#    mydll.write_message(handle, yy)

#test_ecu(mydll, handle, wid)

#print send_data(mydll, handle, wid, [0x22, 0xe6, 0x20])
#print send_data(mydll, handle, wid, [0x22, 0xe2, 0x1a])

#print send_data(mydll, handle, wid, [0x10, 0x86, 0x10, 0x03, 0x0D, 0x0, 0x3, 0x12])
#yy = pointer(SFFMessage())
#mydll.DbgLineToSFF("IDH: 07, IDL: 60, Len: 08, Data: 10 86 10 03 0d 00 62 30 ,TS: 17342,BAUD: 205", yy)
#mydll.PrintSFF(yy,0)
#mydll.write_message(handle, yy)
#time.sleep(1)

# normal, adj, prog
if do_diagnostic_session(mydll, handle, wid, "prog"):
    print "Started diagnostic session"
    time.sleep(1)
do_security_access(mydll, handle, wid)

#while True:
#    print send_data(mydll, handle, wid, [0x27, 0x01])
#    print send_data(mydll, handle, wid, [0x27, 0x02, 0xaa, 0xbb, 0xcc])

#do_security_access(mydll, handle, wid)



#do_routine(mydll, handle, wid, 0x0200, [])

#while True:
#print send_data(mydll, handle, wid, [0x31, 0x02, 0x00])


#while True:
#    print do_proprietary(mydll, handle, wid, 0x3c, [0x7f])


#print send_data(mydll, handle, wid, [0x2e, 0xe2, 0x1a, 0x42, 0x4C, 0x31, 0x54])

#
# sjb put to sleep.  Must be stopped, continues working at speed.  need prog session
#
#while True:
#    send_data(mydll, handle, wid, [0x7e, 0x80])
#    time.sleep(.1)
#   
#print send_data(mydll, handle, wid, [0x2e, 0xe6, 0x20, 66, 76, 56, 84, 45, 49, 52, 67, 54, 51, 54, 45, 65, 66, 0, 0, 0, 0, 0,0,0,0,0,0])


#
# pam download mini-firmware (based on pam_prog_2.dat)
# First do "prog" and sec access
#
#if do_download_compliant(mydll, handle, wid, 0x0, 'PAM_00000000inf4.firmware'):
#if do_download_compliant(mydll, handle, wid, 0x0, 'pam_ret.firmware'):
#if do_download_compliant(mydll, handle, wid, 0x0, 'pam_inf_loop.firmware'):
#if do_download_compliant(mydll, handle, wid, 0x0, 'try_send_can.bin'):
#	do_routine(mydll, handle, wid, 0x0301, [0x00, 0x00, 0x30, 0x00])
#	do_routine(mydll, handle, wid, 0xff00, [0x00, 0x00, 0x0C, 0x00, 0x00, 0x00, 0x00, 0xC0])
# do more downloading and stuffs but I skip that for now....
#	do_routine(mydll, handle, wid, 0x0304, [])

# do when you want to do
#	send_data(mydll, handle, wid, [0x11, 0x81])



#
# sjb download mini-firmware
#

if do_download(mydll, handle, wid, 0x0, '726_000000-again.firmware'):
    print do_proprietary(mydll, handle, wid, 0xb2, [0x01])
    do_download(mydll, handle, wid, 0x7fc000, '726_007fc0-again.firmware')
#    do_download(mydll, handle, wid, 0x7fc000, '726_007fc0-bad.firmware')
    send_data(mydll, handle, wid, [0x11,0x01])
#    time.sleep(1)
    
send_data(mydll, handle, wid, [0x10, 0x81])
#send_data(mydll, handle, wid, [0x22, 0xE6, 0x20])
#send_data(mydll, handle, wid, [0x22, 0xE6, 0x20])
#send_data(mydll, handle, wid, [0x22, 0xE6, 0x20])
    

#print pull_data_14230(mydll, handle, wid, 0x0, 0x10)
#print pull_data_14230(mydll, handle, wid, 0x7fc000, 0x10)
#for i in range(0,32):
#    print do_read_memory_14430(mydll, handle, wid, 1<<i, 0x10)

#print send_data(mydll, handle, wid, [0x22, 0xe6, 0x20])


#print send_data(mydll, handle, wid, [0x34, 0x00, 0x7f, 0xc0, 0, 0x01, 0, 0, 0x10])
#print send_data(mydll, handle, wid, [0x36, 0x0F, 0x0E, 0x42, 0x4C, 0x38, 0x54, 0x2D, 0x31, 0x34, 0x43, 0x36, 0x33, 0x36, 0x2D, 0x41, 0x42])
#time.sleep(1)
#print send_data(mydll, handle, wid, [0x37])

#print send_data(mydll, handle, wid, [0x35, 0x00, 0, 0, 0, 0, 0, 0x10])



#while True:
#    print send_data(mydll, handle, wid, [0x22, 0x02, 0x0])
#   time.sleep(.1)
    
#brake stuff
#
#while True:
#    print do_proprietary(mydll, handle, wid, 0x2b, [0xff, 0xff]) # slow can't stop, fast nothing - 22 (couldn't start diagnostic session!)
#while True:
#    print do_proprietary(mydll, handle, wid, 0x3c, [0x7f]) # when stopped, brakes engaged.

#send_data(mydll, handle, wid, [0x10, 0x81])
#print do_proprietary(mydll, handle, wid, 0x01a3, [3])

#for x in range(0,256):
#    do_routine_14230(mydll, handle, wid, 0x02, [x])
#do_routine_14230(mydll, handle, wid, 0x31, [0])
#while True:
#    do_routine_14230(mydll, handle, wid, 0xf0, [0])


#for x in range(0,0xffff):
#    do_proprietary(mydll, handle, wid, x, [])
#    do_proprietary(mydll, handle, wid, x, [3])
#    do_proprietary(mydll, handle, wid, x, [0, 0])
#    do_proprietary(mydll, handle, wid, x, [0, 0, 0])
#    do_proprietary(mydll, handle, wid, x, [0, 0, 0, 0])

#for x in range(0,256):
#    do_proprietary(mydll, handle, wid, 0x3c, [x])

#while True:
#    do_proprietary(mydll, handle, wid, 0x3c, [0xff])



#send_data(mydll, handle, wid, [0x31,02,00])

#do_inputoutput(mydll, handle, wid, 0x030e, [0x03, 0x00, 0x00])
#do_inputoutput(mydll, handle, wid, 0x116b, [0x03, 0x00, 0x00])
#do_inputoutput(mydll, handle, wid, 0x0307, [0x03, 0x00, 0x00])
#do_inputoutput(mydll, handle, wid, 0x1166, [0x03, 0x00, 0x00])  # works in drive

#for x in [0x0307,0x030e,0x03bc,0x1166,0x1167,0x116b,0x1e09,0x1e53,0x1e54,0x1e55,0x1e56]:
#        do_inputoutput(mydll, handle, wid, x, [0x03,0,0])
#        raw_input('next')

#for x in range(0,0xff):
#    do_inputoutput(mydll, handle, wid, 0x1167, [0x03, x, x]) 

#for x in range(0, 0x256):
#    if do_inputoutput_14230(mydll, handle, wid, x, [0x03]):
#        print "0 args"
#    if do_inputoutput_14230(mydll, handle, wid, x, [0x03,0x00]):
#        print "1 args"
#    if do_inputoutput_14230(mydll, handle, wid, x, [0x03,0x00,0x00]):
#        print "2 args"
#    if do_inputoutput_14230(mydll, handle, wid, x, [0x03,0x00,0x00,0x00]):
#        print "3 args"
#    if do_inputoutput_14230(mydll, handle, wid, x, [0x03,0x00,0x00,0x00,0x00]):
#        print "4 args"

#ret = send_data(mydll, handle, wid, [0x10,0xf0])
#do_security_access2(mydll,handle,wid)

#search_for_readable_memory(mydll, handle, wid)
#search_for_pullable_memory(mydll, handle, wid)

#for x in range(0, 0xffff):
#    do_read_memory_14430(mydll, handle, wid, x<<8, 0x10)

# length 6 says out of range
# otherwise its out of range
#send_data(mydll, handle, wid, [0xb1,0x0,0x0])
#try_ids(mydll, handle, wid)



#print "%x" % len(pull_data(mydll, handle, wid, 0x7f000, 0x10))

#print do_read_memory(mydll, handle, wid, 0x0100c0, 0x10)
#do_write_memory(mydll, handle, wid, 0x0100f0, [0,1,2,3,4,5,6,7,8,9,1,2,3,4,5,6])

# 1 - (00000001)
# 4 - (00000100)

#do_routine(mydll, handle, wid, 0x402a, [])
#do_routine(mydll, handle, wid, 0x4044, [0xff])


#send_data(mydll, handle, 0x7e0, [0x10,0x83])
#send_data(mydll, handle, 0x7e0, [0x85,0x01])
#send_data(mydll, handle, 0x7e0, [0x31,0x01,0x02,0x02])

#for x in range(0, 0xffff):
#    print "%04X " % x,
#    do_routine(mydll, handle, wid, 0x0436, [(x&0xff) >> 8, x&0xff])
#    time.sleep(1)


#kill_engine(mydll, handle, 1000)

#for x in range(1,0xffff):
#    do_routine(mydll, handle, wid, x, [])


#for x in range(0,0xffff):
#    do_routine_14230_by_address(mydll, handle, wid, x<<8,[])

#for x in range(0,256):
#    do_routine_14230(mydll, handle, wid, x, [0])
#    do_routine_14230(mydll, handle, wid, x, [0,0])
#    do_routine_14230(mydll, handle, wid, x, [0,0,0])
#    do_routine_14230(mydll, handle, wid, x, [0,0,0,0])


#do_routine_14230(mydll, handle, wid, 0x02, [0])
#do_routine_14230(mydll, handle, wid, 0x31, [0])
#do_routine_14230(mydll, handle, wid, 0xf0, [0])

#for x in range(0,256):
#    resp = do_routine_14230_get_response(mydll, handle, wid, 0xf0, [x])
#    print resp

#for x in range(0,0xffff):
#    do_routine(mydll, handle, wid , x, [0,0xe5])
#for x in range(0,0xffff):
#    do_inputoutput(mydll, handle, wid, x, [])

#for x in range(0,0xff):
#    do_inputoutput_14230(mydll, handle, wid, x, [])

mydll.close_device(handle)
