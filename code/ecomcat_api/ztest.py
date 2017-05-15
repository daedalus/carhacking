from PyEcom import *
from config import *
import time, struct, sys, binascii

def str_to_hexarr(val):
    payload = []
    for x in val:
        payload.append(ord(x))

    return payload

def nbo_int_to_bytearr(dword):
    arr = []
    arr.append(dword & 0xFF)
    arr.append((dword >> 8) & 0xFF)
    arr.append((dword >> 16) & 0xFF)
    arr.append((dword >> 24) & 0xFF)

    return arr

class EcuPart:
    def __init__(self, address, write_address, length):
        self.address = address
        self.write_address = write_address
        self.length = length

if __name__ == "__main__":

    ecom = PyEcom('Debug\\ecomcat_api')
    ecom.open_device(1,35916)

    ECU = 0x750

    #SmartKey 0x750 [0xB5] seems to return 34 when ret[2] - 0xAB

    for i in range(0, 1000):
        ret = ecom.send_iso_tp_data(0x750, [0x27, 0x01], 0x40)
        #key = (ret[2] - 0xAB) & 0xFF
        #key = (~ret[2] + 1) & 0xFF
        key = i & 0xFF
        ret = ecom.send_iso_tp_data(0x750, [0x27, 0x02, key], 0x40)

        if ret[2] != 0x35:
            print "New Error: %d %d" % (key, i)
            break

    ret = ecom.request_upload_14229(ECU, 0x01, 0x44, 0x0000F000, 0x00000001, 0x40)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x33, 0x0000F000, 0x00000001, 0x40)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x24, 0x0000F000, 0x00000001, 0x40)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x22, 0x0000F000, 0x00000001, 0x40)
    ret = ecom.request_upload_14229(ECU, 0x01, 0x12, 0x0000F000, 0x00000001, 0x40)

    #Potential values for 34715300
    #val = ecom.toyota_dword_to_targetdata(0xD2363456), 
    #val = ecom.toyota_dword_to_targetdata(0x0E5E5B29)
    #val = ecom.toyota_dword_to_targetdata(0x6F8C9954)
    #val = ecom.toyota_dword_to_targetdata(0x423659A8)

    #val = ecom.toyota_targetdata_to_dword("42353B3C3A4A4948")
    #print "34715100 %08X" % (val)

    #T-0008-08.cuw
##    val = ecom.toyota_targetdata_to_dword("443637373B3B384A")
##    print "34702000 %08X" % (val)  
##
##    val = ecom.toyota_targetdata_to_dword("443345463B3C484B")
##    print "34702100 %08X" % (val)  
##
##    val = ecom.toyota_targetdata_to_dword("443A45453B3D4839")
##    print "34702200 %08X" % (val)  
##
##    val = ecom.toyota_targetdata_to_dword("443A33493B3D4B4D")
##    print "34705000 %08X" % (val)
##
##    val = ecom.toyota_targetdata_to_dword("443246363B463B49")
##    print "34705100 %08X" % (val)
##
##    val = ecom.toyota_targetdata_to_dword("444632463B473D4B")
##    print "34705200 %08X" % (val)
##
##    val = ecom.toyota_targetdata_to_dword("4231333A3A384B3E")
##    print "34705300 %08X" % (val)
##
##    #T-009-08.cuw
##    val = ecom.toyota_targetdata_to_dword("4437483B3B483F3D")
##    print "34709000 %08X" % (val)
##
##    val = ecom.toyota_targetdata_to_dword("424539363A363749")
##    print "34710000 %08X" % (val)
##
##    val = ecom.toyota_targetdata_to_dword("423145393A38484C")
##    print "34710100 %08X" % (val)
##
##    #T-0052-11.cuw
##    val = ecom.toyota_targetdata_to_dword("423438493A3E3E4D")
##    print "34715000 %08X" % (val)
##
##    val = ecom.toyota_targetdata_to_dword("42353B3C3A4A4948")
##    print "34715100 %08X" % (val)
##
##    val = ecom.toyota_targetdata_to_dword("424433493A4B4B4D")
##    print "34715200 %08X" % (val)
##    print "CRC32: %08X" % (binascii.crc32("34715200") & 0xFFFFFFFF)
##
##    #T-0053-11.cuw
##    val = ecom.toyota_targetdata_to_dword("3042384539373E39")
##    print "34728000 %08X" % (val)        
    
##
##    #T-0146-10
##    val = ecom.toyota_targetdata_to_dword("3638393449353A37")
##    print "F152647127 %08X" % (val)
##    #print "CRC32: %08X" % (binascii.crc32("F152647127") & 0xFFFFFFFF)
##
##    val = ecom.toyota_targetdata_to_dword("3638463749353839")
##    print "F152647126 %08X" % (val)
##    #print "CRC32: %08X" % (binascii.crc32("F152647126") & 0xFFFFFFFF)
##
##    val = ecom.toyota_targetdata_to_dword("363846394935383C")
##    print "F152647125 %08X" % (val)
##    #print "CRC32: %08X" % (binascii.crc32("F152647125") & 0xFFFFFFFF)       

##
##    f = open("toyota_ecu.bin", "rb")
##
##    num = 1
##    total_blocks = []
##
##    chunk = f.read(0x400)
##    if chunk:
##        hex_arr = str_to_hexarr(chunk)
##        total_blocks += hex_arr
##
##        #datalen = len(hex_arr)
##        datalen = 0x400
##        
##
##        print "%04X" % (datalen)
##
##        datalen = datalen & 0x0FFF
##        data_bytes = (0x01000 | datalen) & 0x0FFFF
##        byteone = (data_bytes >> 8)
##        bytetwo = data_bytes & 0xFF
##
##        print "%02X %02X" % (byteone, bytetwo)
##        
##        #print "[%d] -> Len: %d" % (num, len(hex_arr))
##        #print hex_arr
##        num += 1
##
##    print "Total: %X" % (len(total_blocks))
##
##    vindex = 0
##    cnt = 0
##    chunks = len(total_blocks) / 0x100
##
##
##    for i in range(0, chunks):
##        print "Count: %d" % (cnt)
##        
##        tmp = total_blocks[vindex:vindex+0x100]
##        vindex += 0x100
##        cnt += 1
##        for asdf in tmp:
##            sys.stdout.write("%02X " % (asdf))
##
##    ecu1 = EcuPart(0x00000000, 0xFF000000, 0x1000)
##    ecu2 = EcuPart(0xF7000100, 0xFF001000, None)
##
##
##    addrs = [0x00000000, 0xF7000100]
##    write_addrs = [0xFF000000, 0xFF001000]
##
##    lens = {}
##    lens[addrs[0]] = 0x1000
##
##    addr_arr = nbo_int_to_bytearr(write_addrs[0])
##    print hex(addr_arr[0])
##    print hex(addr_arr[1])
##    print hex(addr_arr[2])
##    print hex(addr_arr[3])
##
##    f.close()
