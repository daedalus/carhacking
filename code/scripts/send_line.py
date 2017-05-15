from subprocess import call
filename = "drive_twitch.dat"

print "Sending data from %s" % (filename)

lines = []
f = open(filename, "r")
for line in f:
    print "Calling Ecomcat %s" % (line)
    call(["Ecomcat.exe", "\"" + line + "\""])
    #print "Hit enter to continue"
    #yesno = raw_input("Hit enter to continue")

