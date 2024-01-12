import sys
from SFF import SFFMessage

filea_ids = []
fileb_ids = []
if (len(sys.argv) < 3):
    print(f"Usage: {sys.argv[0]} <file1> <file2>")
    sys.exit(1)

file_a = sys.argv[1]
file_b = sys.argv[2]

with open(file_a) as fpfilea:
    for line in fpfilea:
        sff_msg = SFFMessage(line.strip())
        if(sff_msg.wid not in filea_ids):
            filea_ids.append(sff_msg.wid)
print("Found %d ids in %s" % (len(filea_ids), file_a))

with open(file_b) as fpfileb:
    for line in fpfileb:
        sff_msg = SFFMessage(line.strip())
        if(sff_msg.wid not in fileb_ids):
            fileb_ids.append(sff_msg.wid)
print("Found %d ids in %s\n" % (len(fileb_ids), file_b))

fileb_ids_diff = [wid for wid in fileb_ids if wid not in filea_ids]
filea_ids_diff = [wid for wid in filea_ids if wid not in fileb_ids]
print(f"Only {file_a}")
for wid in filea_ids_diff:
    print(wid)

print(f"Only {file_b}")
for wid in fileb_ids_diff:
    print(wid)
