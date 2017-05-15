from PyEcom import *
from config import *
from ctypes import *
import time, struct

if __name__ == "__main__":
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,35916)

    #Engine ECU
    ECU = 0x7E0

    for i in range(0, 11):
        print "Attempt %d" % (i)
        resp = ecom.send_iso_tp_data(ECU, ecom.get_security_access_payload(ECU), None)

        if not resp or len(resp) == 0:
            print "No Response"

        seed = resp[2] << 24 | resp[3] << 16 | resp[4] << 8 | resp[5]

        #obviously incorrect
        key = [0,0,0,0]

        key_data = [0x27, 0x02, key[0], key[1], key[2], key[3]]

        key_resp = ecom.send_iso_tp_data(ECU, key_data, None)
        err = ecom.get_error(key_resp)
        if err != 0x00:
            print "Error: %s" % (NegRespErrStr(err))
