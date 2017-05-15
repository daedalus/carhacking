import sys, getopt
from SFF import SFFMessage

verbose = True
outputfile = ""
optlist, args = getopt.getopt(sys.argv[1:], ':o:')
if(len(args) < 1):
    print "Usage: %s [options] <inputfile> <id>"
    print "options:"
    print " -o <output file>"
    sys.exit(1)

for o,a in optlist:
    if o == "-o":
        outputfile = a

inputfile = args[0]
search_byte = args[1]
found_lines = []
fp = open(inputfile, "r")

#look for the 2nd byte of the data for a particular byte
for line in fp:
    msg = SFFMessage(line)

    #skip over multi-line transactions as we don't care
    if msg.data[0:1] == "2":
        continue

    if msg.data[3:5] == search_byte:
        found_lines.append(msg)    
fp.close()

if(outputfile != ""):
    fp = open(outputfile, "w")
    
for msg in found_lines:
    print str(msg)

    if(outputfile != ""):
        fp.write(str(msg) + '\n')
fp.close()
