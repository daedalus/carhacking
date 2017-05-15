#!/usr/bin/python
import sys
import difflib
import binascii
from SFF import SFFMessage

file_a = sys.argv[1]
file_b = sys.argv[2]
download = sys.argv[3] # something like NEW DOWNLOAD  00 44 00 01 00 08 00 06 FF F8

fa = open(file_a)
fb = open(file_b)
fc = open('output', 'wb')

aline = fa.readline()
while aline.find(download) < 0:
	aline = fa.readline()

bline = fb.readline()
while bline.find(download) < 0:
	bline = fb.readline()


def print_line(line):
	global fc
	i = 9 
	while i < len(line):
		bbyte = binascii.a2b_hex(line[i:i+2])
		fc.write(bbyte)
		i+=3

aline = fa.readline()
bline = fb.readline()

quit = False
while aline and not quit:
	if aline != bline:
		alen = int(aline[:3], 16)
		blen = int(bline[:3], 16)
		if alen > blen:
			print_line( aline.strip())
		else:
			print_line( bline.strip())
	else:
		print_line( aline.strip())
	aline = fa.readline()
	bline = fb.readline()
        if aline.find('NEW DOWNLOAD') >= 0:
		quit = True

fc.close()
