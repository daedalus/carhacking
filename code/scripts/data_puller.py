import sys
from SFF import SFFMessage

if __name__ == "__main__":

    if(len(sys.argv) < 3):
        print "Usage: %s <inputfile> <outputfile> <11-bit CAN ID>" % (sys.argv[0])
        print "Example1: %s input.dat output.dat 0025" % (sys.argv[0])
        print "Example2: %s input.dat output.dat 0025,0026,0027" % (sys.argv[0])
        print "Example3: %s input.dat output.dat 0025-02FF" % (sys.argv[0])
        sys.exit(1)

    #search types
    #1 == single ID
    #2 == multi-id
    #3 == range
    wid_search = 1
    wids = []
    low = 0
    high = 0
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    find_wid = sys.argv[3]

    if(find_wid.find(',') != -1):
        ids = find_wid.split(",")
        for wid in ids:
            wids.append(wid.strip())
        wid_search = 2
    elif(find_wid.find("-") != -1):
        ids = find_wid.split("-")
        low = int(ids[0].strip(), 16)
        high = int(ids[1].strip(), 16)
        wid_search = 3 

    #input file to read debug lines from
    f = file(input_file, "r")
        
    msgs = []
    count = 0
    for line in f:
        msg = SFFMessage(line)
        if(msg.wid != 0):
            if(wid_search == 1):
                if(msg.wid == find_wid):
                    count += 1
                    msgs.append(line)
                    #msgs.append(msg)
            elif(wid_search == 2):
                if(msg.wid in wids):
                    count += 1
                    msgs.append(line)
                    #msgs.append(msg)
            elif(wid_search == 3):
                wid = int(msg.wid, 16)
                if(wid >= low and wid <= high):
                    count += 1
                    msgs.append(line)
                    #msgs.append(msg)
    f.close()

    #output file to write certain lines out
    f = file(output_file, "w")
        
    for found in msgs:
        f.write(str(found))
        
    f.close()

    print "Found %d messages that match %s" % (count, sys.argv[3])
    
