s_line = "S3210008371065ABCE1F8AB401C8C72967230C6F99B6C84AE25ED793F949CE76CCCC8B"

data_checksum = 0
s_type = s_line[0:2]
s_len = int(s_line[2:4], 16)

data_checksum += s_len
print "SLen: %02X" % (s_len)

curr_index = 4

data_end = 2 * 2
if s_type == "S2":
    data_end = 3 * 2
elif s_type == "S3":
    data_end = 4 * 2

end_index = curr_index + data_end

#addr = int(s_line[curr_index:end_index], 16)
#data_checksum += addr

#print "SLen: %08X" % (addr)

#curr_index = end_index

data = s_line[curr_index:-2]

print data

#create a checksum
for i in range(0, len(data), 2):
    byte = data[i:i+2]

    data_checksum += int(byte, 16)

print "ChecksumByte: 0x%02X" % (~data_checksum & 0xFF)
