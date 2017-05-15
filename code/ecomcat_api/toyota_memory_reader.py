from PyEcom import *
from config import *
import time, struct

if __name__ == "__main__":
    #print "[*] Starting diagnostics check..."
    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,35916)

    #Engine
    #ECU = 0x7E0

    #Hybrid/Power Management
    #ECU = 0x7E2

    #ABS
    ECU = 0x7B0

    ret = ecom.security_access(ECU)

    ret = ecom.request_upload_14229(ECU, 0x01, 0x44, 0x0000F000, 0x00000001)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x33, 0x0000F000, 0x00000001)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x24, 0x0000F000, 0x00000001)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x22, 0x0000F000, 0x00000001)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x12, 0x0000F000, 0x00000001)
    
    ret = ecom.request_upload_14230(ECU, 0x01, 0x0000F000, 0x00000001)

    ret = ecom.read_memory_14229(ECU, 0x44, 0x0000F000, 0x00000001)
    ret = ecom.read_memory_14229(ECU, 0x24, 0x0000F000, 0x00000001)
    ret = ecom.read_memory_14229(ECU, 0x33, 0x0000F000, 0x00000001)
    ret = ecom.read_memory_14229(ECU, 0x12, 0x0000F000, 0x00000001)

    ret = ecom.read_memory_14230(ECU, 0x0000F000, 0x00000001)
