#!/usr/bin/python

import sys
from SFF import SFFMessage

filea_ids = []
filea_ids_diff = []
fileb_ids = []
fileb_ids_diff = []

if(len(sys.argv) < 2):
    	print "Usage: %s <file1> " % (sys.argv[0])
	sys.exit(1)

file_a = sys.argv[1]

fpfilea = open(file_a)

stats = {}

for line in fpfilea:
    	sff_msg = SFFMessage(line.strip())
	if int(sff_msg.idh,16) == 0 and int(sff_msg.idl,16) == 0x81:
		data = sff_msg.data
		wheel1 = int(data[0:2],16)<<8
		wheel2 = (int(data[3:5],16))
		wheel = wheel1 + wheel2
		x = "%d" % wheel
		try:
			print x + stats[80] + stats[82] + stats[215]
		except:
			pass
        if int(sff_msg.idh,16) == 0 and int(sff_msg.idl,16) == 0x80:
                data = sff_msg.data
                wheel1 = int(data[0:2],16)<<8
                wheel2 = (int(data[3:5],16))
                wheel = wheel1 + wheel2
		wheel1 = int(data[6:8],16)<<8
                wheel2 = (int(data[9:11],16))
		wheel2 = wheel1 + wheel2
		stats[80] = ",%d,%d" % (wheel, wheel2)
        if int(sff_msg.idh,16) == 0 and int(sff_msg.idl,16) == 0x82:
		data = sff_msg.data
                wheel1 = int(data[0:2],16)
		stats[82] = ",%d" % wheel1
        if int(sff_msg.idh,16) == 0x02 and int(sff_msg.idl,16) == 0x15:
                data = sff_msg.data
                wheel1 = int(data[0:2],16)<<8
                wheel2 = (int(data[3:5],16))
                v1 = wheel1 + wheel2
                wheel1 = int(data[6:8],16)<<8
                wheel2 = (int(data[9:11],16))
                v2 = wheel1 + wheel2
                wheel1 = int(data[12:14],16)<<8
                wheel2 = (int(data[15:17],16))
                v3 = wheel1 + wheel2
                wheel1 = int(data[18:20],16)<<8
                wheel2 = (int(data[21:23],16))
                v4 = wheel1 + wheel2
		stats[215] = ",%d,%d,%d,%d" % (v1,v2,v3,v4)


fpfilea.close()

