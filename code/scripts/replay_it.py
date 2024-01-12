from subprocess import call

#globals
#x = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]
#x = []

def playit(x):
        filename = "temp.dat"
        with open(filename, "w") as fp:
                for line in x:
                        fp.write(line + "\n")
        print(f"Running => ECOMCat {filename}")
        call(["ECOMCat.exe", filename])
        #print "Please hit enter to continue"
        #ch = sys.stdin.readline()

def find_first(x,cur,level):
        temp = x[cur:]
        playit(temp)
        offset = len(x)/level
        print("in findit with cur = %d, level=%d, offset=%d" % (cur, level,offset))
        yesno = input("Did it still do the thing?")
        if yesno[0] == 'y':
                # didn't need those bytes
                cur += offset
        else:
                if offset == 0:
                        cur -= 1
                cur -= offset

        if offset > 0:
                return find_first(x,cur,2*level)
        print("FOUND BEGINING")
        print(x[cur])
        return cur

def find_end(x,cur,level):
        temp = x[:cur]
        playit(temp)
        offset = len(x)/level
        print("in findit with cur = %d, level=%d, offset=%d" % (cur, level,offset))
        yesno = input("Did it still do the thing?")
        if yesno[0] == 'y':
                # didn't need those bytes
                if offset == 0:
                        cur -=1
                cur -= offset
        else:
                cur += offset

        if offset > 0:
                return find_end(x,cur,2*level)
        print("FOUND END")
        print(x[cur])
        return cur


def findit(x):
        # pad out to power of 2
        counter = 1
        dalen = len(x)
        while dalen > 2:
                dalen /= 2
                counter += 1
        y = len(x)
        while y < 2**(counter+1):
                x += [x[len(x)-1]]
                y += 1
        first = find_first(x, len(x)/2, 4)
        last = find_end(x, len(x)/2, 4)
        print("FOUND MINIMAL SET")

        with open("minset.dat", "w") as min_fp:
                for l in x[first:last+1]:
                        min_fp.write(l + "\n")

        #print x[first:last+1]

if __name__ == "__main__":
        #get array 'lines' which is everyline from a debug output
        lines = []
        with open('input_good.dat', 'r') as fp:
                print("starting..")
                lines.extend(line.strip() for line in fp)
        findit(lines)
