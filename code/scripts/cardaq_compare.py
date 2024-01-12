import sys, getopt
from SFF import SFFMessage

output = ""

optlist, args = getopt.getopt(sys.argv[1:], ':o:')
if (len(args) < 2):
    print(f"Usage: {sys.argv[0]} [options] <cardaq.dat> <real_cap.dat>")
    sys.exit(1)

for o, a in optlist:
    #output mode to a file
    if o == "-o":
        output = a

filea_msgs = []
fileb_msgs = []
fileb_msgs_diff = []
file_a = args[0]
file_b = args[1]

with open(file_a) as fplock:
    for line in fplock:
        #msg = SFFMessage(line)
        if(line not in filea_msgs):
            filea_msgs.append(line)
print("[*] FileA parsed...")

i = 0
with open(file_b) as fplock:
    for line in fplock:
        #msg = SFFMessage(line)
        if(line not in fileb_msgs):
            fileb_msgs.append(line)
print("[*] FilesB parsed...")

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


if(of):
    of.close()
