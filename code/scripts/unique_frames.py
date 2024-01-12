import sys, getopt
from SFF import SFFMessage

verbose = True
outputfile = ""
optlist, args = getopt.getopt(sys.argv[1:], ':o:')
if(len(args) < 1):
    print("Usage: %s [options] <inputfile>")
    print("options:")
    print(" -o <output file>")
    sys.exit(1)

for o,a in optlist:
    if o == "-o":
        outputfile = a

inputfile = args[0]
with open(inputfile, "r") as fp:
    unique_msgs = []
    total = 0

    for line in fp:
        msg = SFFMessage(line)
        total = total + 1
        if msg not in unique_msgs:
            unique_msgs.append(msg)
print("File had %d lines and %d were unique" % (total, len(unique_msgs)))

if(outputfile != ""):
    fp = open(outputfile, "w")

for msg in unique_msgs:
    print(msg)

    if(outputfile != ""):
        fp.write(str(msg) + '\n')
fp.close()
