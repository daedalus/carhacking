import sys

while(1):
    sys.stdout.write("Enter CAN Data: ")
    line = sys.stdin.readline()
    line = line.strip()

    #Hit q to quit
    if(line == "q" or line == "Q"):
        break

    payload = []
    for x in line.split(' '):
        payload.append(int(x, 16))

    print "N) Normal A) AckData D) AckDataAck"
    sys.stdout.write("Enter Msg Type: ")
    msg_type = sys.stdin.readline()
    msg_type = msg_type.upper().strip()

    print payload
    print msg_type
