import sys, os, getopt
from SFF import SFFMessage
from subprocess import call

def Histogram(L):
    d = {}
    for x in L:
        sff_id = x.wid
        if sff_id in d:
            d[sff_id] += 1
        else:
            d[sff_id] = 1
    return d

if __name__ == "__main__":

    output_file = ""
    input_file = ""
    create_id_files = False
    try_ecomcat = False

    optlist, args = getopt.gnu_getopt(sys.argv[1:], ':o:ce')

    if(len(args) < 1):
        print "Usage: %s [options] <inputfile> [flags]" % (sys.argv[0])
        print "Options:"
        print " -o <outputfile>"
        print "Flags:"
        print " -c Create ID files from histogram"
        print " -e Run ID files created with '-c' through ECom cable"
        sys.exit(1)

    #print optlist
    #print args

    for o, a in optlist:
        if o == "-o":
            output_file = a
        if o == "-c":
            create_id_files = True
        if o == "-e":
            try_ecomcat = True

    #get the arguments
    input_file = args[0]
        
    f = file(input_file, "r")

    out_f = None
    if(output_file != ""):
        out_f = file(output_file, "w")

    msgs = []
    for line in f:
        msg = SFFMessage(line)
        if(msg.wid != 0):
            msgs.append(msg)
        
    histo = Histogram(msgs)
    sff_codes = []

    for sff_code in sorted(histo, key=histo.get, reverse=True):
        if(output_file):
            out_f.write("%s %s\n" % (sff_code, histo[sff_code]))
        
        print sff_code, histo[sff_code]
        sff_codes.append(sff_code)

    if(out_f):
        out_f.close()

    if(create_id_files):
        input_name = os.path.splitext(input_file)[0]
        for sff_code in sff_codes:
            output_file = input_name + "_" + sff_code + ".dat"  
            call(["python", "data_puller.py", input_file, output_file, sff_code])

            if(try_ecomcat):
                print "Running => ECOMCat %s" % (output_file)
                call(["ECOMCat.exe", output_file])
                #print "Please hit enter to continue"
                #ch = sys.stdin.readline()
    
