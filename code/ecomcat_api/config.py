#2010 Toyota Prius ECU Information

#Flashing information
(RcvAckData, RcvAckDataAck) = range(0,2)

#Prius encryption keys (These should stay in the same order due to the algo)
PriusSecrets = [0xA441, 0x2172, 0xA421, 0x4172]

#coalesced versions of above for easy XOR'ing
PriusSecret1 = 0xA4412172
PriusSecret2 = 0xA4214172

#EffectiveKeys same as doing the XORs with the above
#but less steps
PriusEffectiveKey = 0x00606000
PriusABSKey = 0x00252500

#Sometimes starting a diagnostic session is
#done with 0x5F, rather than the standard of 0x2
PriusDiagCode = 0x5F

PriusMainBodyID = 0x750

#Toyota Prius 2010 ECU IDs (a.k.a. wid) 
TP_Transmission = 0x727
TP_AirBag = 0x780
TP_PreCollision1 = 0x781
TP_Radar = 0x790
TP_PreCollision2 = 0x791
TP_EPMS = 0x7A1
TP_APGS = 0x7A2
TP_ABS = 0x7B0
TP_ComboMeter = 0x7C0
TP_AC = 0x7C4
TP_Nav = 0x7D0
TP_ECT = 0x7E0
TP_Hybrid = 0x7E2

#NEEDED 0xE0
#Sub-ECU IDs for Prius 'Main Body' ECU (0x750)
TP_LKA = 0x02
TP_MainBody = 0x40
TP_PM1 = 0x57
TP_PM2 = 0x58
TP_HLAutoLevel = 0x70
TP_DDoor = 0x90
TP_PDoor = 0x91
TP_RRDoor = 0x92
TP_RLDoor = 0x93
TP_SR = 0xAD
TP_SmartKey = 0xB5
TP_RemoteStart = 0xB6
TP_MainSwitch = 0xEC
TP_PowerSource = 0xE9

#Prius ECU to String name table (Main body is in another section)
PriusECU = {
    TP_Transmission: "Transmission",
    TP_AirBag: "AirBag",
    TP_PreCollision1: "Pre-Collision",
    TP_Radar: "Radar",
    TP_PreCollision2: "Pre-Collision 2",
    TP_EPMS: "EPMS",
    TP_APGS: "APGS - Park Assist",
    TP_ABS: "ABS - Anti-Lock Braking",
    TP_ComboMeter: "Combo Meter",
    TP_AC: "Air Conditioning",
    TP_Nav: "Navigation",
    TP_ECT: "ECT - Engine",
    TP_Hybrid: "Hybrid System",
}
PriusMainECU = {
    TP_LKA: "Lane Keep Assist (LKA)",
    TP_MainBody: "Main Body",
    TP_PM1: "PM1 Gateway",
    TP_PM2: "PM2 Gateway",
    TP_HLAutoLevel: "Headlamp Autolevel",
    TP_DDoor: "Driver Door",
    TP_PDoor: "Passenger Door",
    TP_RRDoor: "Rear Right Door",
    TP_RLDoor: "Rear Left Door",
    TP_SR: "Sliding Roof",
    TP_SmartKey: "Smart Key",
    TP_RemoteStart: "Remote Engine Starter",
    TP_MainSwitch: "Main Switch",
    TP_PowerSource: "Power Source Control",
}
#Diagnostic custom payloads
PriusDiagData = {TP_ABS: [0x10, 0x01]}
#SecurityAccess custom payloads
PriusSAData = {TP_ABS: [0x27, 0x01, 0x00]}
#Hopefully
PriusEffectiveKeys = {TP_ABS: 2434304}
#These are InputOutputControlByLocalIdentifier (0x30). See 14230-3.pdf 
#Prius Commands
PriusCMD = {
    "Seat_Belt_Drive": {
        'Desc': "Engage driver's seatbelt motor",
        'ID': TP_PreCollision1,
        'Data': [0x30, 0x01, 0x00, 0x01],
    },
    "Fuel_Cut_All": {
        'Desc': "Cut fuel to all cylinders",
        'ID': TP_ECT,
        'Data': [0x30, 0x1C, 0x00, 0x0F, 0xA5, 0x01],
    },
}
#These are InputOutputControlByLocalIdentifier (0x30). See 14230-3.pdf 
#These all use WID 0x750 with the first data byte being the SubID
PriusMBCMD = {
    "Headlamps_On": {
        'Desc': "Turn off the head lamps",
        'SubID': TP_MainBody,
        'Data': [0x30, 0x15, 0x00, 0x40, 0x00],
    },
    "Headlamps_Off": {
        'Desc': "Turn off the head lamps (Only works if in Auto-Mode)",
        'SubID': TP_MainBody,
        'Data': [0x30, 0x15, 0x00, 0x00, 0x00],
    },
    "Horn_On": {
        'Desc': "Horn activated for several seconds",
        'SubID': TP_MainBody,
        'Data': [0x30, 0x06, 0x00, 0x20],
    },
    "Horn_Off": {
        'Desc': "Deactivate Horn",
        'SubID': TP_MainBody,
        'Data': [0x30, 0x06, 0x00, 0x00],
    },
    "Lock_All_Doors": {
        'Desc': "Lock All Doors",
        'SubID': TP_MainBody,
        'Data': [0x30, 0x11, 0x00, 0x80, 0x00],
    },
    "Unlock_All_Doors": {
        'Desc': "Unlock All Doors",
        'SubID': TP_MainBody,
        'Data': [0x30, 0x11, 0x00, 0x40, 0x00],
    },
    "Unlock_Hatch": {
        'Desc': "Unlock the Hatch",
        'SubID': TP_MainBody,
        'Data': [0x30, 0x11, 0x00, 0x00, 0x80],
    },
}
#2010 Ford Escape
FordDiagCode = 0x02

#Escape ECU to string name table
FordECU = {
    1793: "GPSM",
    1824: "IC",
    1830: "SJB",
    1831: "ACM",
    1840: "PSCM",
    1843: "HVAC",
    1846: "PAM",
    1847: "RCM",
    1888: "ABS",
    1889: "4x4",
    1893: "OCSM",
    1958: "FDIM",
    1959: "FCIM",
    2000: "APIM",
    2016: "PCM",
}






