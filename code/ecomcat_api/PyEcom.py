from ctypes import *
import time, binascii
from iso14229 import *
from config import *

class SFFMessage(Structure):
    _fields_ = [("IDH", c_ubyte),
                ("IDL", c_ubyte),
                ("data", c_ubyte * 8),
                ("options", c_ubyte),
                ("DataLength", c_ubyte),
                ("TimeStamp", c_uint),
                ("baud", c_ubyte)]

class PyEcom:
    
    def __init__(self, dllname):
        self.mydll = CDLL(dllname)
        self.handle = None

    def open_device(self, baud, serial):
        #self.handle = self.mydll.open_device(1,0)
        self.handle = self.mydll.open_device(baud, serial)

    def data_to_line(self, data, linelen):
            line = ''
            x = 0
            while x < len(data):
                    line += "%02X " % data[x]
                    x += 1

            while x < linelen:
                    line += "00 "
                    x += 1

            return line

    def get_pretty_print(self, data):
        line = ""

        for ch in data:
            line += "%02X " % (ch)

        return line

    def get_error(self, data, error_index=0x2):
        if(data[0] == 0x7F):
            if(len(data) >= error_index):
                return data[error_index]
        else:
            return 0x00

    def send_iso_tp_data_encap(self, wid, data, byte_id):
        sff_msg = pointer(SFFMessage())
        idh = (wid & 0xff00) >> 8
        idl = (wid & 0xff)

        if len(data) > 6:
            #print "Multi packet"

            # first packet
            datalen = len(data)
            byteone = 0x10 + (0xf00 & datalen)
            bytetwo = 0xff & datalen
            firstdata = [byteone, bytetwo] + data[0:5]
            line = "IDH: %02X, IDL: %02X, Len: 08, Data: %02X " % (idh, idl, byte_id)
            line += self.data_to_line(firstdata, 8)
            self.mydll.DbgLineToSFF(line, sff_msg)
            self.mydll.PrintSFF(sff_msg,0)
            self.mydll.write_message(self.handle, sff_msg)

            #response
            read_by_wid = self.mydll.read_message_by_wid_with_timeout
            read_by_wid.restype = POINTER(SFFMessage)
            sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+8, 1000)

            if not sff_resp:
                print "No Response"
                return []

            sent = 5
            counter = 0
            self.mydll.PrintSFF(sff_resp,0)
            
            if sff_resp.contents.data[1] != 0x30:
                    print "Bad response"
                    return []

            #send the remaining data
            while sent < datalen:
                firstbyte = 0x20 + ((counter+1) & 0xf)
                firstdata = [firstbyte] + data[5 + counter*6 : 13 + counter*6]
                line = "IDH: %02X, IDL: %02X, Len: 08, Data: %02X " % (idh, idl, byte_id)
                line += self.data_to_line(firstdata, 8)
                self.mydll.DbgLineToSFF(line, sff_msg)
                self.mydll.PrintSFF(sff_msg,0)
                self.mydll.write_message(self.handle, sff_msg)
                sent += 6
                counter += 1                

        else:
            #print "Single packet"
            line = "IDH: %02X, IDL: %02X, Len: 08, Data: %02X %02X " % (idh, idl, byte_id, len(data))
            line += self.data_to_line(data, 8) 
            self.mydll.DbgLineToSFF(line, sff_msg)
            self.mydll.PrintSFF(sff_msg,0)
            self.mydll.write_message(self.handle, sff_msg)

        read_by_wid = self.mydll.read_message_by_wid_with_timeout
        read_by_wid.restype = POINTER(SFFMessage)

        sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+8, 1000)

        #if you can not read a message, return nothing
        if not sff_resp:
            return []

        #Since the 1st byte will be the ID, skip over it
        self.mydll.PrintSFF(sff_resp,0)
        first_byte = sff_resp.contents.data[1]

        #account for the waiting response on slow actions
        if first_byte < 0x8:
            # is it a slow operation?
            while sff_resp.contents.data[2] == 0x7f and sff_resp.contents.data[4] == 0x78:
                    time.sleep(.1)
                    sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+8, 1000)
                    if not sff_resp:
                            return []
                    self.mydll.PrintSFF(sff_resp,0)
            return sff_resp.contents.data[2:]

        toread = ((first_byte & 0xf) << 8) + sff_resp.contents.data[2]
        total_to_read = toread
        toread -= 5
        ret = sff_resp.contents.data[3:]
        self.mydll.DbgLineToSFF("IDH: %02X, IDL: %02X, Len: 08, Data: %02X 30 00 00 00 00 00 00" % (idh, idl, byte_id), sff_msg)
        self.mydll.PrintSFF(sff_msg,0)
        self.mydll.write_message(self.handle, sff_msg)

        while( toread > 0 ):
            sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+8, 1000)
            toread -= 6
            print sff_resp.contents.data
            ret += sff_resp.contents.data[2:]
            self.mydll.PrintSFF(sff_resp,0)
        return ret[:total_to_read]

    def recv_iso_tp_data(self, wid):
        sff_msg = pointer(SFFMessage())
        
        read_by_wid = self.mydll.read_message_by_wid_with_timeout
        read_by_wid.restype = POINTER(SFFMessage)        

        ret = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+1, 500)

        if not ret:
            return []

        self.mydll.PrintSFF(ret,0)

        return ret.contents.data[1:]

    def send_message(self, line):
        sff_msg = pointer(SFFMessage())

        self.mydll.DbgLineToSFF(line, sff_msg)
        self.mydll.PrintSFF(sff_msg,0)
        self.mydll.write_message(self.handle, sff_msg)        
    
    def send_iso_tp_data(self, wid, data, byte_id=None, AckType=None):

        #XXX This should really be integrated, but not for now
        if(byte_id):
            return self.send_iso_tp_data_encap(wid, data, byte_id)
        
        sff_msg = pointer(SFFMessage())
        idh = (wid & 0xff00) >> 8
        idl = (wid & 0xff)

        resp_index = 8
        if(wid in [1,2,3]):
            resp_index = 1
        

        #multi-packet send
        if len(data) > 7:
            #print "Multi packet"

            # first packet
            datalen = len(data)

            # Fix due to Charlie bricking my ECM Booo charlie
            datalen = datalen & 0x0FFF
            data_bytes = (0x01000 | datalen) & 0x0FFFF
            byteone = (data_bytes >> 8)
            bytetwo = data_bytes & 0xFF
            
            firstdata = [byteone, bytetwo] + data[0:6]
            line = "IDH: %02X, IDL: %02X, Len: 08, Data: " % (idh, idl)
            line += self.data_to_line(firstdata, 8)
            self.mydll.DbgLineToSFF(line, sff_msg)
            self.mydll.PrintSFF(sff_msg,0)
            self.mydll.write_message(self.handle, sff_msg)

            #response
            read_by_wid = self.mydll.read_message_by_wid_with_timeout
            read_by_wid.restype = POINTER(SFFMessage)
            sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+resp_index, 1000)
            sent = 6
            counter = 0

            if sff_resp:
                self.mydll.PrintSFF(sff_resp,0)
                if sff_resp.contents.data[0] != 0x30:
                        print "Bad response"
                        return []
            else:
                return []

            #send the remaining data
            while sent < datalen:
                    firstbyte = 0x20 + ((counter+1) & 0xf)
                    firstdata = [firstbyte] + data[6 + counter*7 : 13 + counter*7]
                    line = "IDH: %02X, IDL: %02X, Len: 08, Data: " % (idh, idl)
                    line += self.data_to_line(firstdata, 8)
                    self.mydll.DbgLineToSFF(line, sff_msg)
                    self.mydll.PrintSFF(sff_msg,0)
                    self.mydll.write_message(self.handle, sff_msg)
                    sent += 7
                    counter += 1                

        else:
            #print "Single packet"
            line = "IDH: %02X, IDL: %02X, Len: 08, Data: %02x " % (idh, idl, len(data))
            line += self.data_to_line(data, 8) 
            self.mydll.DbgLineToSFF(line, sff_msg)
            self.mydll.PrintSFF(sff_msg,0)
            self.mydll.write_message(self.handle, sff_msg)

        #get the response
        read_by_wid = self.mydll.read_message_by_wid_with_timeout
        read_by_wid.restype = POINTER(SFFMessage)

        sff_resp = None
        if(wid in [1,2,3]):
            if(AckType != None):
                read_by_wid_ack = self.mydll.read_message_by_wid_get_ack_timeout
                read_by_wid_ack.restype = POINTER(SFFMessage)
                sff_resp = self.mydll.read_message_by_wid_get_ack_timeout(self.handle, wid+resp_index, AckType, 1000)
            else:
                sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+resp_index, 1000)
        else:
            sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+resp_index, 1000)

        #if you can not read a message, return nothing
        if not sff_resp:
            return []

        self.mydll.PrintSFF(sff_resp,0)
        first_byte = sff_resp.contents.data[0]

        #account for the waiting response on slow actions
        if first_byte < 0x8:
            # is it a slow operation?
            while sff_resp.contents.data[1] == 0x7f and sff_resp.contents.data[3] == 0x78:
                    time.sleep(.1)

                    if(wid in [1,2,3]):
                        sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+1, 1000)
                    else:
                        sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+8, 1000)
                        
                    if not sff_resp:
                            return []
                    self.mydll.PrintSFF(sff_resp,0)
            return sff_resp.contents.data[1:]

        toread = ((first_byte & 0xf) << 8) + sff_resp.contents.data[1]
        total_to_read = toread
        toread -= 6
     
        ret = sff_resp.contents.data[2:]
        self.mydll.DbgLineToSFF("IDH: %02X, IDL: %02X, Len: 08, Data: 30 00 00 00 00 00 00 00" % (idh, idl), sff_msg)
        self.mydll.PrintSFF(sff_msg,0)
        self.mydll.write_message(self.handle, sff_msg)
        while( toread > 0 ):
            sff_resp = self.mydll.read_message_by_wid_with_timeout(self.handle, wid+resp_index, 1000)
            toread -= 7
            ret += sff_resp.contents.data[1:]
            self.mydll.PrintSFF(sff_resp,0)
        return ret[:total_to_read]

    def toyoyta_fix_checksum(self, idh, idl, data_len, data):
        checksum = 0

        checksum = idh + idl + data_len
        for d_byte in data:
            checksum += d_byte

        return checksum & 0xFF

    def get_diagnostic_payload(self, wid):
        if wid in PriusDiagData:
            return PriusDiagData[wid]
        else:
            return [0x10, 0x01]

    def get_security_access_payload(self, wid):
        if wid in PriusSAData:
            return PriusSAData[wid]
        else:
            return [0x27, 0x01]
        
    def diagnostic_session(self, wid, data=[0x10, 0x01], byte_id=None):
        ret = None
        index = 0

        ret = self.send_iso_tp_data(wid, data, byte_id)
            
        if not ret:
            return False

        if ret[0] == 0x50:
            return True

        if ret[2] == 0x78:
            read_by_wid = self.mydll.read_message_by_wid_with_timeout
            read_by_wid.restype = POINTER(SFFMessage)
            sff_resp = mydll.read_message_by_wid_with_timeout(self.handle, wid+8, 1000)

            self.mydll.PrintSFF(sff_resp,0)
            if sff_resp.contents.data[1] == 0x50:
                return True

        err = self.get_error(ret)
        if err != 0x00:
            print "Error: %s" % (NegRespErrStr(err))
            return False

    def toyota_getstatus(self, wid):
        ret = self.send_iso_tp_data(wid, [0x50], None, RcvAckData)
        self.recv_iso_tp_data(wid)

        return ret

    def toyota_loop_getstatus(self, wid, bad_id, ok_id=None):
        i = 0
        while(True):
            ret = self.send_iso_tp_data(wid, [0x50], None, RcvAckData)
            self.recv_iso_tp_data(wid)

            #unexpected return status should be dealt with
            if(ret[0] != bad_id):
                if(ret[0] != 0x00):
                    if(ok_id != None and ret[0] == ok_id):
                        return ""
                    else:
                        return ret[0]
            
            if(ret[0] == bad_id):
                time.sleep(1)
            else:
                return ""   

    def toyota_targetdata_to_dword(self, str_target_data):
        data = str_target_data

        if len(data) % 2 != 0:
            print "TargetData must have an EVEN number of characters"

        j = 0
        total = ""
        for i in range(0, len(data), 2):
            byte = data[i:i+2]

            val = int(byte, 16)

            #checksum style thing?
            val = val - j

            total += chr(val)

            #each byte is subtracted by the iterator
            j += 1

        total = int(total, 16)

        #print "%04X" % (total)

        return total

    def toyota_dword_to_targetdata(self, dword):

        shifter = 28
        add = 0
        targetdata = ""

        #break out each nibble
        while shifter >= 0:
            nibble = (dword >> shifter) & 0xF

            str_nibble = "%1X" % (nibble)

            hex_str_nibble = "%2X" % (ord(str_nibble) + add)

            targetdata += hex_str_nibble

            add += 1
            shifter -= 4

        print targetdata
        return targetdata

    def toyota_cracker(self, wid, data=[0x27, 0x01], byte_id=None):
        ret = None
        i = 0
        found_key = False
        seed = 0x0000
        prev_seed = 0x0000

        #start diagnostic session first
        ret = self.diagnostic_session(wid, [0x10, 0x01], byte_id)
        if(not ret):
            print "[!] Diagnostic Session: Failed"
            return False

        resp = self.send_iso_tp_data(wid, data, byte_id)        
        
        if not resp or len(resp) == 0:
            print "No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error: %s" % (NegRespErrStr(err))
            return False

        #constants when calculating keys are taken from the response
        const_1 = resp[2]
        const_2 = resp[5]

        prev_seed = seed
        seed = (resp[3] << 8) | resp[4]

##            if prev_seed == 0x0000:
##                prev_seed = seed
##            else:
##                if prev_seed != seed:
##                    f = open("Seeds.txt", "a+")
##                    print "[!] Key Changed"
##                    pretty_arr = self.get_pretty_print(resp[3:5])
##                    pretty_arr = pretty_arr.replace(' ', '')
##                    f.write(pretty_arr + '\n')
##                    f.close()
##                    return False


        #i guess start at half the seed is a good place? 
        key_guess = seed / 2

        while(i < 0x20):

            i += 1
            #break key_guess into 2 pieces
            guess_1 = (key_guess & 0xFF00) >> 8
            guess_2 = key_guess & 0x00FF

            #print "Guess1: %02X Guess2: %02X" % (guess_1, guess_2)

            key_data = [0x27, 0x02, const_1, guess_1, guess_2, const_2]
            if(byte_id):
                key_data = [0x27, 0x02, guess_1, guess_2]

            resp = self.send_iso_tp_data(wid, key_data, byte_id)
            if(resp[0] == 0x67):
                found_key = True
                print "Found the KEY: %02X %02X" % (guess_1, guess_2)
            else:
                err = self.get_error(resp)
                if err != 0x35 and err != 0x36:           
                    print "Error: %s" % (NegRespErrStr(err))
                    return False

            key_guess = (key_guess + 1) & 0xFFFF

        return found_key

    #XXX This function is deprecated and is only presnt to provide a representation
    #of the code taken from the cuw.exe binary, just use 'security_access()' below
    def toyota_key_from_seed(self, seed):

        num_of_secrets = len(PriusSecrets)
        if(len(seed) != num_of_secrets):
            print "SeedKey Mismatch: SeedLen: %d Number of Secrets: %d" % (len(seed), num_of_secrets)
            return []

        print "Seed: %s" % (self.get_pretty_print(seed))
        for i in range(0, num_of_secrets):
            #print "%04X" % (PriusSecrets[i])

            #get the first two bytes of the seed 
            seed_short = seed[0] << 8 | seed[1]
            #print "%04X" % (seed_short)

            #XOR the first two bytes of the seed with the first secret
            key_piece = PriusSecrets[i] ^ seed_short
            #print "%04X" % (key_piece)

            #replace the first 2-bytes with the last 2
            seed[0] = seed[2]
            seed[1] = seed[3]

            #put the newly generated key_piece in the last 2 bytes
            seed[2] = key_piece >> 8 & 0xFF
            seed[3] = key_piece & 0xFF

            print "Key: %02X %02X %02X %02X" % (seed[0], seed[1], seed[2], seed[3])

        #print "Key: %02X %02X %02X %02X" % (seed[0], seed[1], seed[2], seed[3])
        return seed

    def security_access(self, wid, byte_id=None):
        ret = None

        #ret = self.diagnostic_session(wid, self.get_diagnostic_payload(wid), byte_id)
        #if(not ret):
        #    print "[!] Diagnostic Session: Failed"
        #    return False

        resp = self.send_iso_tp_data(wid, self.get_security_access_payload(wid), byte_id)

        if not resp or len(resp) == 0:
            print "No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error: %s" % (NegRespErrStr(err))
            return False
        elif err == 0x00:
            if resp[2] == 0 and resp[3] == 0 and resp[4] == 0 and resp[5] == 0:
                print "Already authenticated"
                return True

        #generate the key from the seed and the secrets
        seed = 0
        seed = resp[2] << 24 | resp[3] << 16 | resp[4] << 8 | resp[5]
        #print "Seed: %04X" % (seed)
        key_dword = seed ^ PriusEffectiveKey
        if wid in PriusEffectiveKeys:
            eff_key = PriusEffectiveKeys[wid]
            #print "Using Effective Key: %04X" % (eff_key)
            key_dword = seed ^ eff_key

        #print "Key: %04X" % (key_dword)
             
        #key = self.toyota_key_from_seed(resp[2:6])
        key = [0,0,0,0]
        key[0] = key_dword >> 24 & 0xFF
        key[1] = key_dword >> 16 & 0xFF
        key[2] = key_dword >> 8 & 0xFF
        key[3] = key_dword & 0xFF

        key_data = [0x27, 0x02, key[0], key[1], key[2], key[3]]

        #send they key to the server
        seed = self.send_iso_tp_data(wid, key_data, byte_id)
        err = self.get_error(seed)
        if err != 0x00:
            print "Error: %s" % (NegRespErrStr(err))
            return False
            
        return True

    def routine_control(self, wid, subfunc, routine_id, byte_id=None):

        #break the rountine ID into bytes
        msb_rid = (routine_id >> 8) & 0xFF
        lsb_rid = routine_id & 0xFF
        
        resp = self.send_iso_tp_data(wid, [0x31, subfunc, msb_rid, lsb_rid], byte_id)
        if not resp or len(resp) == 0:
            print "No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error: %s" % (NegRespErrStr(err))
            return False

        return True

    #Address length: 3-bytes
    #Size length: 1-byte
    def read_memory_14230(self, wid, address, size, byte_id=None):
        #The total payload sent to the ECU
        payload = []

        #Add the SID
        payload.append(0x23)

        for i in range(3, 0, -1):
            shifter = (i * 8) - 8
            addr_byte = (address >> shifter) & 0xFF
            payload.append(addr_byte)

        payload.append(size & 0xFF)

        resp = self.send_iso_tp_data(wid, payload, byte_id)
        if(not resp or len(resp) == 0):
            print "RequestUpload: No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error[0x%02X]: %s" % (err, NegRespErrStr(err))
            return False

        return True  

    def read_memory_14229(self, wid, addrAndLenFormat, address, size, byte_id=None):
        #The total payload sent to the ECU
        payload = []

        #Add the SID
        payload.append(0x23)

        #addressAndLengthFormatIdentifier = 1 byte
        #XY => X is the length (in bytes) of the address and y is the length (in bytes) of the address
        alFormat = addrAndLenFormat & 0xFF
        payload.append(alFormat)

        #get the size and address length formats
        addr_format = alFormat & 0x0F
        size_format = (alFormat & 0xF0) >> 4 

        for i in range(addr_format, 0, -1):
            shifter = (i * 8) - 8
            addr_byte = (address >> shifter) & 0xFF
            payload.append(addr_byte)

        for i in range(size_format, 0, -1):
            shifter = (i * 8) - 8
            size_byte = (size >> shifter) & 0xFF
            payload.append(size_byte)

        resp = self.send_iso_tp_data(wid, payload, byte_id)
        if(not resp or len(resp) == 0):
            print "RequestUpload: No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error[0x%02X]: %s" % (err, NegRespErrStr(err))
            return False

        return True            
        

    def request_upload_14229(self, wid, dataFormatID, addrAndLenFormat, address, size, byte_id=None):

        #The total payload for this request
        payload = []

        #ID for RequestUploadService
        payload.append(0x35)

        #dataFormatIdentifier == 1 byte
        #XY => X is 'compressionMethod' and Y is 'encryptingMethod'
        #00 == no compression or encryption
        fID = dataFormatID & 0xFF
        payload.append(fID)

        #addressAndLengthFormatIdentifier = 1 byte
        #XY => X is the length (in bytes) of the address and y is the length (in bytes) of the address
        alFormat = addrAndLenFormat & 0xFF
        payload.append(alFormat)

        #break out 
        addr_format = alFormat & 0x0F
        size_format = (alFormat & 0xF0) >> 4 

        for i in range(addr_format, 0, -1):
            shifter = (i * 8) - 8
            addr_byte = (address >> shifter) & 0xFF
            payload.append(addr_byte)

        for i in range(size_format, 0, -1):
            shifter = (i * 8) - 8
            size_byte = (size >> shifter) & 0xFF
            payload.append(size_byte)            

        resp = self.send_iso_tp_data(wid, payload, byte_id)
        if(not resp or len(resp) == 0):
            print "RequestUpload: No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error[0x%02X]: %s" % (err, NegRespErrStr(err))
            return False

        return True

    def request_upload_14230(self, wid, dataFormatID, address, size, byte_id=None):

        #The total payload for this request
        payload = []

        #ID for RequestUploadService
        payload.append(0x35)

        for i in range(3, 0, -1):
            shifter = (i * 8) - 8
            addr_byte = (address >> shifter) & 0xFF
            payload.append(addr_byte)

        #dataFormatIdentifier == 1 byte
        #XY => X is 'compressionMethod' and Y is 'encryptingMethod'
        #00 == no compression or encryption
        fID = dataFormatID & 0xFF
        payload.append(fID)

        for i in range(3, 0, -1):
            shifter = (i * 8) - 8
            size_byte = (size >> shifter) & 0xFF
            payload.append(size_byte)            

        resp = self.send_iso_tp_data(wid, payload, byte_id)
        if(not resp or len(resp) == 0):
            print "RequestUpload: No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error[0x%02X]: %s" % (err, NegRespErrStr(err))
            return False

        return True

    def transfer_data(wid, block_seq_counter):
        payload = []
        payload.append(0x36)

        payload.append(block_seq_counter)

        resp = self.send_iso_tp_data(wid, payload, None)

        if(not resp or len(resp) == 0):
            print "RequestUpload: No Response"
            return False

        err = self.get_error(resp)
        if err != 0x00:
            print "Error[0x%02X]: %s" % (err, NegRespErrStr(err))
            return []

        return resp[1:]

    def transfer_exit(wid):
        resp = self.send_iso_tp_data(wid, [0x37], None)
        if err != 0x00:
            print "Error[0x%02X]: %s" % (err, NegRespErrStr(err))
            return False

        return True
