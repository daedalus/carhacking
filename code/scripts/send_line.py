from subprocess import call
filename = "drive_twitch.dat"

print(f"Sending data from {filename}")

lines = []
f = open(filename, "r")
for line in f:
    print(f"Calling Ecomcat {line}")
    call(["Ecomcat.exe", "\"" + line + "\""])
    #print "Hit enter to continue"
    #yesno = raw_input("Hit enter to continue")

