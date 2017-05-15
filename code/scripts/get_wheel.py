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
for line in fpfilea:
    	sff_msg = SFFMessage(line.strip())
	if int(sff_msg.idh,16) == 0 and int(sff_msg.idl,16) == 0x81:
		data = sff_msg.data
		wheel1 = int(data[0:2],16)<<8
		wheel2 = (int(data[3:5],16))
		wheel = wheel1 + wheel2
		print wheel
fpfilea.close()

