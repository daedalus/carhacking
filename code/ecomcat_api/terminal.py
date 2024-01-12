import sys

while 1:
    sys.stdout.write("Enter CAN Data: ")
    line = sys.stdin.readline()
    line = line.strip()

    #Hit q to quit
    if line in ["q", "Q"]:
        break

    payload = [int(x, 16) for x in line.split(' ')]
    print("N) Normal A) AckData D) AckDataAck")
    sys.stdout.write("Enter Msg Type: ")
    msg_type = sys.stdin.readline()
    msg_type = msg_type.upper().strip()

    print(payload)
    print(msg_type)
