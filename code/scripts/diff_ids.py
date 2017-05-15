import sys
from SFF import SFFMessage

filea_ids = []
filea_ids_diff = []
fileb_ids = []
fileb_ids_diff = []

if(len(sys.argv) < 3):
    print "Usage: %s <file1> <file2>" % (sys.argv[0])
    sys.exit(1)

file_a = sys.argv[1]
file_b = sys.argv[2]

fpfilea = open(file_a)
for line in fpfilea:
    sff_msg = SFFMessage(line.strip())
    if(sff_msg.wid not in filea_ids):
        filea_ids.append(sff_msg.wid)
fpfilea.close()

print "Found %d ids in %s" % (len(filea_ids), file_a)

fpfileb = open(file_b)
for line in fpfileb:
    sff_msg = SFFMessage(line.strip())
    if(sff_msg.wid not in fileb_ids):
        fileb_ids.append(sff_msg.wid)
fpfileb.close()

print "Found %d ids in %s\n" % (len(fileb_ids), file_b)

for wid in fileb_ids:
    if wid not in filea_ids:
        fileb_ids_diff.append(wid)

for wid in filea_ids:
    if wid not in fileb_ids:
        filea_ids_diff.append(wid)

print "Only %s" % (file_a) 
for wid in filea_ids_diff:
    print wid

print "Only %s" % (file_b) 
for wid in fileb_ids_diff:
    print wid
