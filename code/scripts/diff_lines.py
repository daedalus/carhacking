import sys, getopt
from SFF import SFFMessage

output = ""

optlist, args = getopt.getopt(sys.argv[1:], ':o:')
if(len(args) < 2):
    print("Usage: %s [options] <filea> <fileb>" % (sys.argv[0]))
    sys.exit(1)

for o, a in optlist:
    #output mode to a file
    if o == "-o":
        output = a

filea_msgs = []
filea_msgs_diff = []
fileb_msgs = []
fileb_msgs_diff = []
file_a = args[0]
file_b = args[1]

fplock = open(file_a)
for line in fplock:
    msg = SFFMessage(line)
    if(msg not in filea_msgs):
        filea_msgs.append(msg)
fplock.close()

fplock = open(file_b)
for line in fplock:
    msg = SFFMessage(line)
    if(msg not in fileb_msgs):
        fileb_msgs.append(msg)
fplock.close()

for msg in fileb_msgs:
    if not msg in filea_msgs:
        fileb_msgs_diff.append(msg)

for msg in filea_msgs:
    if not msg in fileb_msgs:
        filea_msgs_diff.append(msg)

of = None
if(output != ""):
    of = open(output, "w")
    
filea_cnt = "Only %s [%d lines]" % (file_a, len(filea_msgs_diff))
print(filea_cnt)

if(of):
    of.write(filea_cnt + '\n')

for msg in filea_msgs_diff:
    print(str(msg))
    if(of):
        of.write(str(msg) + '\n')

print("\n")
if(of):
    of.write('\n')

fileb_cnt = "Only %s [%d lines]" % (file_b, len(fileb_msgs_diff))
print(fileb_cnt)

if(of):
    of.write(fileb_cnt + '\n')
    
for msg in fileb_msgs_diff:
    print(str(msg))
    if(of):
        of.write(str(msg) + '\n')

if(of):
    of.close()
