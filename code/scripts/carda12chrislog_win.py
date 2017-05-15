if __name__ == "__main__":
    filename = "ecm_flash_attempt2.in"
    f = open(filename)
    arr = []
    i = 0

    f2 = open(filename + ".dat", "w")
    
    for line in f:
        line = line.strip()
        pieces = line.split(',')

        can_data = pieces[3]

        idh = can_data[0:5].replace(' ', '').strip()
        idl = can_data[6:11].replace(' ', '').strip()
        data = can_data[12:].strip()

        f2.write("IDH: %02X, IDL: %02X, Len: %02X, Data: %s\n" % (int(idh, 16), int(idl, 16), 8, data))
