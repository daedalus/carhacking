import sys, struct, binascii

filename = "T-0052-11.cuw"

def FixMotCRC(mot_str):

    if mot_str == "":
        return mot_str
    
    data_checksum = 0
    s_type = mot_str[0:2]
    s_len = int(mot_str[2:4], 16)

    data_checksum += s_len
    #print "SLen: %02X" % (s_len)

    curr_index = 4

    data_end = 2 * 2
    if s_type == "S2":
        data_end = 3 * 2
    elif s_type == "S3":
        data_end = 4 * 2
    else:
        return mot_str

    end_index = curr_index + data_end

    data = mot_str[curr_index:-2]

    #create a checksum
    for i in range(0, len(data), 2):
        byte = data[i:i+2]

        data_checksum += int(byte, 16)

    #print "checksum: %02X" % (~data_checksum & 0xFF)

    return mot_str[0:-2] + "%02X" % (~data_checksum & 0xFF)

fixed_fp = open(filename+".fixed", "wb+")

with open(filename, "rb") as f:
    
    calibration_str = f.read(0x0D)
    fixed_fp.write(calibration_str)
    
    version = f.read(0x01)
    fixed_fp.write(version)

    header_body_crc32 = struct.unpack('>L', f.read(0x04))[0]    
    fixed_fp.write(struct.pack('>L', header_body_crc32))

    file_len = struct.unpack('>L', f.read(0x04))[0]
    fixed_fp.write(struct.pack('>L', file_len))
    
    application_name_len = struct.unpack('>H', f.read(0x02))[0]
    fixed_fp.write(struct.pack('>H', application_name_len))

    application_name = f.read(application_name_len)
    fixed_fp.write(application_name)

    header_len = struct.unpack('>L', f.read(0x04))[0]
    fixed_fp.write(struct.pack('>L', header_len))

    saved_header_pos = f.tell()

    header_crc32 = struct.unpack('>L', f.read(0x04))[0]

    header = f.read(header_len)

    header_crc32_fixed = binascii.crc32(header)

    fixed_fp.write(struct.pack('>l', header_crc32_fixed))
    fixed_fp.write(header)

    print "Header CRC: %08X" % (header_crc32)
    print "Header Computed CRC: %08X" % (header_crc32_fixed & 0xFFFFFFFF)

    #should match the 'Number' in the CUW header
    number_of_cpus = f.read(0x01)
    fixed_fp.write(number_of_cpus)

    version_txt_file_len = struct.unpack('>H', f.read(0x02))[0]
    fixed_fp.write(struct.pack('>H', version_txt_file_len))

    version_txt_file = f.read(version_txt_file_len)
    fixed_fp.write(version_txt_file)

    s_format_len = header_len = struct.unpack('>L', f.read(0x04))[0]
    fixed_fp.write(struct.pack('>L', s_format_len))

    s_format_crc32 = header_len = struct.unpack('>L', f.read(0x04))[0]

    s_format_data = f.read(s_format_len)
    s_format_lines = s_format_data.split('\n')
    new_s_format_data = ""
    for s_line in s_format_lines:
        new_line = FixMotCRC(s_line.strip())
        new_s_format_data += new_line + "\r\n"

    #get rid of the last \r\n
    new_s_format_data = new_s_format_data[0:-2]

    s_format_crc32_fixed = binascii.crc32(new_s_format_data)
    fixed_fp.write(struct.pack('>l', s_format_crc32_fixed))

    fixed_fp.write(new_s_format_data)

    print "Header CRC: %08X" % (s_format_crc32)
    print "Header Computed CRC: %08X" % (s_format_crc32_fixed)


fixed_fp.seek(0x12)
cuw_bytes = fixed_fp.read()
cuw_crc32 = binascii.crc32(cuw_bytes)

fixed_fp.seek(0x0E)
fixed_fp.write(struct.pack('>l', cuw_crc32))

fixed_fp.close()





