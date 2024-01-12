import sys, getopt
from SFF import SFFMessage

output = ""

optlist, args = getopt.getopt(sys.argv[1:], ':o:')
if (len(args) < 2):
    print(f"Usage: {sys.argv[0]} [options] <filea> <fileb>")
    sys.exit(1)

for o, a in optlist:
    #output mode to a file
    if o == "-o":
        output = a

filea_msgs = []
fileb_msgs = []
file_a = args[0]
file_b = args[1]

with open(file_a) as fplock:
    for line in fplock:
        msg = SFFMessage(line)
        if(msg not in filea_msgs):
            filea_msgs.append(msg)
with open(file_b) as fplock:
    for line in fplock:
        msg = SFFMessage(line)
        if(msg not in fileb_msgs):
            fileb_msgs.append(msg)
fileb_msgs_diff = [msg for msg in fileb_msgs if msg not in filea_msgs]
filea_msgs_diff = [msg for msg in filea_msgs if msg not in fileb_msgs]
of = open(output, "w") if (output != "") else None
filea_cnt = "Only %s [%d lines]" % (file_a, len(filea_msgs_diff))
print(filea_cnt)

if(of):
    of.write(filea_cnt + '\n')

for msg in filea_msgs_diff:
    print(msg)
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
    print(msg)
    if(of):
        of.write(str(msg) + '\n')

if(of):
    of.close()
