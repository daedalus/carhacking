if __name__ == "__main__":
    filename = "cardaq_flash_attemp1.dat"
    f = open(filename)
    arr = []
    i = 0
    for line in f:
        line = line.strip()
        if(line.startswith("\__")):
            line = line.replace("\__", "").strip()
            arr.append(line)

    f.close()
    f2 = open(filename + ".cvl", 'w')

    for line in arr:
        byte_vals = line.split(' ')
        data_len = len(byte_vals) - 4 #this will take out the CAN ID

        data = ""
        for b in byte_vals[4:]:
            data += "%s " % (b)

        idh = int(byte_vals[2], 16)
        idl = int(byte_vals[3], 16)

        if(byte_vals[0] == "00" and byte_vals[1] == "00"):
            #print "IDH: %02X, IDL: %02X, Len: %02X, Data: %s" % (idh, idl, data_len, data)
            f2.write("IDH: %02X, IDL: %02X, Len: %02X, Data: %s\n" % (idh, idl, data_len, data))
        else:
            print "29-bit not supported!"

    f2.close()

    print "END"
