import sys, getopt
from SFF import SFFMessage

verbose = True
outputfile = ""
optlist, args = getopt.getopt(sys.argv[1:], ':o:')
if(len(args) < 1):
    print "Usage: %s [options] <inputfile>"
    print "options:"
    print " -o <output file>"
    sys.exit(1)

for o,a in optlist:
    if o == "-o":
        outputfile = a

inputfile = args[0]
fp = open(inputfile, "r")
unique_wids = []
total = 0

for line in fp:
    msg = SFFMessage(line)
    total = total + 1
    if not msg.wid in unique_wids:
        unique_wids.append(msg.wid)
fp.close()

print "File had %d lines and %d were unique" % (total, len(unique_wids))

if(outputfile != ""):
    fp = open(outputfile, "w")
    
for msg in unique_wids:
    print str(msg)

    if(outputfile != ""):
        fp.write(str(msg) + '\n')
fp.close()
