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

id_strings = {	0x10: "DiagnosticSessionControl",
		0x11: "ECUReset",
		0x27: "SecurityAccess",
		0x28: "CommunicationControl",
		0x3e: "TesterPresent",
		0x83: "AccessTimingParameter",
		0x84: "SecuredDataTransmission",
		0x85: "ControlDTCSetting",
		0x86: "ResponseOnEvent",
		0x87: "LinkControl",
		0x22: "ReadDataByIdentifier",
		0x23: "ReadMemoryByAddress",
		0x24: "ReadScalingDataByIdentifier",
		0x2a: "ReadDataByPeriodicIdentifier",
		0x2c: "DynamicallyDefineDataIdentifier",
		0x2e: "WriteDataByIdentifier",
		0x3d: "WriteMemoryByAddress",
		0x14: "ClearDiagnosticInformation",
		0x19: "ReadDTCInformation",
		0x2f: "InputOutputControlByIdentifier",
		0x31: "RoutineControl",
		0x34: "RequestDownload",
		0x35: "RequestUpload",
		0x36: "TransferData",
		0x21: "readDataByLocalIdentifier",
		0x3b: "writeDataByLocalIdentifier",
		0x37: "RequestTransferExit",
		0x18: "readDiagnosticTroubleCodesByStatus"}

def get_id_string(id):
	prefix = ""
	if (0x10 <= id and id <= 0x3e) or (0x80 <= id and id <= 0xbe):
		prefix = "Request_"

	if (0x50 <= id and id <= 0x7e) or (0xc0 <= id and id <= 0xfe):
		prefix = "PosResponse_"
		id -= 0x40

	if id == 0x7f:
		return "NegResponse"	

        if id_strings.has_key(id):
                id_s = prefix + id_strings[id]
        else:
                id_s = prefix + "UNKNOWN_%02x" % id

	return id_s

def handle_data(payload, len, direction, line_num):
	id = int(payload[0:2],16)
	id_s = get_id_string(id)
	
	payload = payload[2:]
	#print "%sLen %02X, id %02X, payload %s" % (direction_to_string(direction), len, id, payload)
	print id_s + "  Line:%d" % (line_num)
#	if id == 0x34:
#		print "NEW DOWNLOAD " + payload
#	if id == 0x36:
#		print "%x: " % len + payload #[:3]

fpfilea = open(file_a)

### initialize
to_read = 0
current_one = 0
already_read = 0
long_data = ""
long_direction = 0

ISOTP_ENCAP = True
SEEN_ENCAP = False

line_num = 0

for line in fpfilea:
    	sff_msg = SFFMessage(line.strip())
	idh = int(sff_msg.idh,16)
	idl = int(sff_msg.idl,16)

        line_num += 1

	if idh == 7:
#		print line
		direction = toserver
		if idl & 0xf > 0x7:
			direction = toclient

                #get the data from the SFFMessage
		data = sff_msg.data

                #Prius will encapsulate some information
                if( (idl == 0x50 or idl == 0x58) and ISOTP_ENCAP):
                        SEEN_ENCAP = True
                        data = data[3:]
                                    
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
			# flow control
#			if type[1] == '0':
#				print direction_to_string(direction) + "clear to send"
#			else:
#				print direction_to_string(direction) + "wait"
			pass		
		#print data

		SEEN_ENCAP = False
fpfilea.close()

