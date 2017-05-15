#!/usr/bin/python
import sys
from SFF import SFFMessage
clean, longdata = range(2)
toserver, toclient = range(2)

if(len(sys.argv) < 2):
    	print "Usage: %s <file1> " % (sys.argv[0])
	sys.exit(1)

file_a = sys.argv[1]

def direction_to_string(direction):
	if direction == toserver:
		return ">> "
	else:
		return "<< "

def handle_data(payload, payload_len, direction, line_num):
	can_id = int(payload[0:2],16)
	id_s = get_id_string(can_id)
	
	payload = payload[2:]
	#print "%sLen %02X, id %02X, payload %s" % (direction_to_string(direction), len, id, payload)
	print id_s + "  Line:%d" % (line_num)

fpfilea = open(file_a)

### initialize
to_read = 0
current_one = 0
already_read = 0
long_data = ""
long_direction = 0

line_num = 0

for line in fpfilea:
    	sff_msg = SFFMessage(line.strip())
	idh = int(sff_msg.idh,16)
	idl = int(sff_msg.idl,16)

        line_num += 1

	if idh == 00:
#		print line
		direction = toserver
		if idl == 4 or idl == 2:
			direction = toclient

                #get the data from the SFFMessage
		data = sff_msg.data
                                    
                data_type = data[0:2]
                        
		if data_type[0] == '0':
			# single packet
			pkt_len = int(data_type, 16)
			payload = data[3:3+pkt_len*3]
			handle_data(payload, pkt_len, direction, line_num)
	      	if data_type[0] == '1':
			if to_read != 0:
				# didn't finish the last long data transmission
#				print "DIDN'T READ FULL PACKET"
				handle_data(long_data, already_read, long_direction, line_num)
	            	# first frame packet
	             	pkt_len = (int(data_type[1], 16) << 8) + int(data[3:5], 16)
			current_one = 0
			to_read = pkt_len
			already_read = 6
			long_data = data[6:]
			long_direction = direction
#			print "%storead: %x, read: %x, data: %s" % (direction_to_string(direction), len, already_read, long_data)
		if data_type[0] == '2':
			# consecutive frame packet
			if current_one + 1 != int(data_type[1],16) and not (current_one == 0xf and int(data_type[1],16) == 0):
#				print "ERROR - LOST PACKET"		
				pass
			current_one = int(data_type[1],16)
			payload = data[3:]
			read_this_time = min(to_read - already_read, 7)
#			print "read %d" % read_this_time 
			already_read += read_this_time
			long_data += " " + data[3:3+read_this_time*3]
#			print "%storead: %x, read: %x, data: %s" % (direction_to_string(direction), len, already_read, long_data)
			if already_read == to_read:
				handle_data(long_data, to_read, long_direction, line_num)
				to_read = 0

		if data_type[0] == '3':
                        pass		
		#print data

fpfilea.close()

