import sys
from subprocess import call
from SFF import SFFMessage

if(len(sys.argv) < 3):
    print "Usage: %s <file> <percentage>" % (sys.argv[0])
    sys.exit(1)

file_a = sys.argv[1]
percent = int(sys.argv[2])

fpfilea = open(file_a)

numlines = 0
for line in fpfilea:
	numlines += 1
fpfilea.close()

print "Found %d lines in file" % numlines

starting = numlines * percent * .01

print "Starting to replay at line number %d" % starting


fpfileb = open(file_a)
numlines = 0
for line in fpfileb:
	line = line.strip()
	if numlines > starting:
		print line
		line = "\"" + line + "\""
        	#call(["ECOMCat.exe", line])
		print ["ECOMCat.exe", line]
        	print "Please hit enter to continue"
        	ch = sys.stdin.readline()
	numlines += 1
fpfileb.close()

