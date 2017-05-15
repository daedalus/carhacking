import sys
from subprocess import call
from SFF import SFFMessage


pos = 0x4e6b
step_time = "2000"

beg_line = "DH: 00, IDL: 81, Len: 08, Data: "
end_line = " 01 00 00 00 00 00 ,TS: 63,BAUD: 1"

while True:
    pos = pos - 0x20
    high = (pos & 0xff00) >> 8
    low = pos & 0xff
    middle = "%02X %02X" % (high, low)

    line = beg_line + middle + end_line

    print middle
    line = "\"" + line + "\""
    call(["ECOMCat.exe", line, step_time])
    #print ["ECOMCat.exe", line, 5000]
                 
