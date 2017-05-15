#Negative Response Codes (See Annex A.1 in the ISO doc for full list)
generalReject = 0x10
serviceNotSupported = 0x11
subFunctionNotSupported = 0x12
responseTooLong = 0x14
busyRepeatRequest = 0x21
conditionsNotCorrect = 0x22
requestSequenceError = 0x24
requestOutOfRange = 0x31
securityAccessDenied = 0x33
invalidKey = 0x35
exceedNumberOfAttempts = 0x36
requiredTimeDelayNotExpired = 0x37
uploadDownloadNotAccepted = 0x70
generalProgrammingFailure = 0x72
requestCorrectlyReceived_ResponsePending = 0x78
subFuncionNotSupportedInActiveSession = 0x7E
serviceNotSupportedInActiveSession = 0x7F
rpmTooHigh = 0x81
rpmTooLow = 0x82
engineIsRunning = 0x83
engineIsNotRunning = 0x84
shifterLeverNotInPark = 0x90

NegRespCode = {}
NegRespCode[generalReject] = ["GR", "General Reject"]
NegRespCode[serviceNotSupported] = ["SNS", "Service Not Supported"]
NegRespCode[subFunctionNotSupported] = ["SFNS", "Subfunction Not Supported: Service exists but not supported by subfunction"]
NegRespCode[responseTooLong] = ["RTL", "Response Too Long"]
NegRespCode[busyRepeatRequest] = ["BRR", "Busy Repeat Request"]
NegRespCode[conditionsNotCorrect] = ["CNC", "Conditions Not Correct"]
NegRespCode[requestSequenceError] = ["RSE", "Request Sequence Error: Server expectes different sequence of request messages"]
NegRespCode[requestOutOfRange] = ["ROOR", "Request of out Range: There exists a parameter which is out of range"]
NegRespCode[securityAccessDenied] = ["SAD", "Security Access Denied: Either 1) Test conditions not met 2) invalid sequence (try DiagSession) 3) requires unlocking of server"]
NegRespCode[invalidKey] = ["IK", "Invalid Key"]
NegRespCode[exceedNumberOfAttempts] = ["ENOA", "Exceeded Number of Security Access Attempts"]
NegRespCode[requiredTimeDelayNotExpired] = ["RTDNE", "Required Time Delay Not Expired: Client attempting to access security too quickly"]
NegRespCode[uploadDownloadNotAccepted] = ["UDNA", "Upload / Download Not Accepted"]
NegRespCode[generalProgrammingFailure] = ["GPF", "General Programming Failure"]
NegRespCode[requestCorrectlyReceived_ResponsePending] = ["RCRRP", "Request Correctly Received Response Pending: Wait for response"]
NegRespCode[subFuncionNotSupportedInActiveSession] = ["SFNSIAS", "Subfunction Not Supported in Active Session"]
NegRespCode[serviceNotSupportedInActiveSession] = ["SNSIAS", "Service Not Supported in Active Session"]

def NegRespErrStr(err_code):
    if err_code in NegRespCode.keys():
        return NegRespCode[err_code][1]
    else:
        return "Unknown Error %02X" % (err_code)


