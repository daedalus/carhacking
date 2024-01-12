import sys, getopt
from SFF import SFFMessage

if __name__ == "__main__":

    input_file = ""
    output_file = ""

    optlist, args = getopt.getopt(sys.argv[1:], ':o:')
    if(len(args) < 1):
        print("Usage: %s [options] <inputfile>")
        print("options:")
        print(" -o <output file>")
        sys.exit(1)

    for o, a in optlist:
        if o == "-o":
            output_file = a

    input_file = args[0]

    with open(input_file, "r") as fp:
        id_len_matches = []

        for line in fp:
            sff_msg = SFFMessage(line)

            uniq = f"{sff_msg.wid}:{sff_msg.len}"

            if (uniq not in id_len_matches):
                id_len_matches.append(uniq)
    if(output_file != ""):
        fp = open(output_file, "w")

    found_str = "Found %d unique ID and Len matches" % (len(id_len_matches))
    print(found_str)
    if(output_file != ""):
        fp.write(found_str + '\n')

    for item in id_len_matches:
        combo = item.split(':')
        found_id_str = f"ID: {combo[0]} Len: {combo[1]}"
        print(found_id_str)

        if(output_file != ""):
            fp.write(found_id_str + '\n')

        
        
