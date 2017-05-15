#include <stdio.h>
#include <time.h>
#include <string.h>
#include "ecommlib.h"

#define IDH_STATE 1
#define IDL_STATE 2
#define LEN_STATE 3
#define DAT_STATE 4
#define TS_STATE  5
#define END_STATE 6

//Input mode will data from the INFILE to be played 
#define INPUTMODE 0

//The most common mode is used to output data read from the CAN Bus
//Please see FILTERMODE for more refined output
#define OUTPUTMODE 1

//If set will continuously sent the content in the variable 'static_cont_line'
#define CONTSEND 0

//Used for incrementing a certain byte value when doing a CONTSEND
//See the example in the CONTSEND section for more information 
#define LOOPER 0

//Setting this option will translate lines in the 'static_cont_lines' array 
//and send them continuously one after the other
#define MEGABALL 0

//Charlie's method for turning his steering wheel. This can prob be repurposed if necessary
//but most likely is easier to do in python
#define READANDWRITE 0

//This option will take data from INFILE and attempt to send it at the same speed
//that is displayed in the timestamp, hopefully simulating the exact traffic pattern
#define SLOWINPUT 0

//The amount of time to perform the actions above
#define ENDTIME 200000

//0 for no filter
//1 for single filter FILTER_IDH and FILTER_IDL
//2 for multi filter (see CANID_11BIT) 
//3 for IDH only filter
#define FILTERMODE 1

#define FILTER_IDH 0x00
#define FILTER_IDL 0x37

#define OUTFILE "output.dat"
#define INFILE "skid-control-1.dat"

#define MS_BUS_SERIAL 35892
#define LINEMAX 100

BYTE CANID_11BIT[0x7FF]; 

unsigned int htoi (const char *ptr)
{
	unsigned int value = 0;
	char ch = *ptr;

    while (ch == ' ' || ch == '\t')
        ch = *(++ptr);

    for (;;) {

        if (ch >= '0' && ch <= '9')
            value = (value << 4) + (ch - '0');
        else if (ch >= 'A' && ch <= 'F')
            value = (value << 4) + (ch - 'A' + 10);
        else if (ch >= 'a' && ch <= 'f')
            value = (value << 4) + (ch - 'a' + 10);
        else
            return value;
        ch = *(++ptr);
    }
}

int DbgLineToSFF(char *line, SFFMessage *sff)
{
	char state = IDH_STATE;
	char *end = line + strlen(line); 
	char *ts;
	char col = 0; 
	char comma = 0;
	char id[3];
	int data_index = 0; 
	int data_len = 0; 

	while(*line)
	{
		if(!*line) 
			break; 

		sff->baud = CAN_BAUD_500K;
//		printf("'%c' '%c' '%c'\n", line[strlen(line)-2], line[strlen(line)-1], line[strlen(line)]);
		if((line[strlen(line)-1] == '3' && line[strlen(line)-2] == ' ') || (line[strlen(line)-2] == '3' && line[strlen(line)-3] == ' '))
		{
			sff->baud = CAN_BAUD_125K;
		}

		switch(state) 
		{
		case IDH_STATE: 
		case IDL_STATE:
		case LEN_STATE:
			//get rid of white space 
			while(*line && (*line == ' ' || *line == '\t'))
				line++; 

			if(!col)
			{
				if(*line == ':')
					col = 1; 
				break;
			}

			//get the data, should be two chars
			if(line + 2 > end) 
				return 1;
 
			//get the single hex value
			id[0] = *line;
			id[1] = *(line+1);
			id[2] = '\0';

			if(state == IDH_STATE)
			{
				sff->IDH = (BYTE)htoi(id); 
				state = IDL_STATE; 
			}
			else if(state == IDL_STATE)
			{
				sff->IDL = (BYTE)htoi(id);
				state = LEN_STATE; 
			}
			else if(state == LEN_STATE)
			{
				sff->DataLength = (BYTE)htoi(id);
				data_len = sff->DataLength; 
				state = DAT_STATE;
			}

			//increment line by one here (and one at the bottom)
			//to compensate for taking 2 characters from the line
			line++;

			//set states
			col = 0;  
			break;
		case TS_STATE:
			//get rid of white space 
			while(*line && (*line == ' ' || *line == '\t'))
				line++; 

			if(!col)
			{
				if(*line == ':'){
					col = 1;
					ts = line + 2;
				}
				break;
			}

			if(!comma)
			{
				if(*line == ','){
					comma = 1; 
					*line = 0; 
					sff->TimeStamp = atoi(ts); 
					state = END_STATE; 
				}
				break;
			}
	
			//set states
			col = 0;  
			break;
		case DAT_STATE:
			//get rid of white space 
			while(*line && (*line == ' ' || *line == '\t'))
				line++; 

			if(!col)
			{
				if(*line == ':')
					col = 1; 
				break;
			}

			if(line + 2 > end) 
				return 1;

			//get a data value
			id[0] = *line; 
			id[1] = *(line+1);
			id[2] = '\0'; 

			if(data_len - 1 >= 0)
			{
				sff->data[data_index] = (BYTE)htoi(id);
				data_len--; 
				data_index++;
				line++;
			}
			
			if(data_len == 0)
			{
				col = 0;
				state = TS_STATE; 
			}

			line++; 

			break;
		}
		
		line++; 
	}

	return 0; 
}

void PrintEFF(EFFMessage *eff, FILE *fp)
{
	int i = 0; 
	//Display the important fields all on one line
	printf("EID: %08X, Len: %02X, Data: ", eff->ID, eff->DataLength, eff->data);

	if(fp)
		fprintf(fp, "EID: %04X, Len: %02X, Data: ", eff->ID, eff->DataLength);

	for (i = 0; i < eff->DataLength; i++)
	{
		printf("%02X ", eff->data[i]);

		if(fp)
			fprintf(fp, "%02X ",eff->data[i]);
	}

	printf("\n");

	if(fp)
		fprintf(fp, "\n");
}

unsigned short GetFirstDataShort(SFFMessage *sff){
	unsigned short ret;
	if (sff->DataLength < 2){
		printf("Trying to get short from packet with less than 2 bytes of data!");
		return 0;
	}
	ret = sff->data[1];
	ret += sff->data[0] << 8;
	return ret;
}

void CreateWheelPacket(SFFMessage *sff, unsigned short newshort, unsigned long ts){
	if (sff->DataLength != 8){
		printf("Passed in a small sff message to CreateWheelPacket!");
		return;
	}
	sff->IDH = 0;
	sff->IDL = 0x81;
	sff->data[1] = newshort & 0xff;
	sff->data[0] = (newshort & 0xff00) >> 8;
	sff->data[2] = 0x12;
	sff->data[3] = sff->data[4] = sff->data[5] = sff->data[6] = sff->data[7] = 0;
	sff->TimeStamp = ts;
}

void PrintSFF(SFFMessage *sff, FILE *fp)
{
	int i = 0; 
	//Display the important fields all on one line
	printf("IDH: %02X, IDL: %02X, Len: %02X, Data: ", sff->IDH, sff->IDL, sff->DataLength);

	if(fp)
		fprintf(fp, "IDH: %02X, IDL: %02X, Len: %02X, Data: ", sff->IDH, sff->IDL, sff->DataLength);

	for (i = 0; i < sff->DataLength; i++)
	{
		printf("%02X ", sff->data[i]);

		if(fp)
			fprintf(fp, "%02X ",sff->data[i]);
	}
	
	printf(",TS: %d", sff->TimeStamp);
	printf(",BAUD: %d", sff->baud);

	printf("\n");

	if(fp)
	{
		fprintf(fp, ",TS: %d", sff->TimeStamp); 
		fprintf(fp, ",BAUD: %d", sff->baud);
		fprintf(fp, "\n");
	}
}

BYTE SFFChecksum(SFFMessage *sff)
{
	BYTE chsum = 0; 
	int i = 0; 
	BYTE len = sff->DataLength;

	//The general checksum should be a byte-limited value of the:
	//IDH+IDL+LEN+Data[0:LEN]
	chsum += sff->IDH;
	chsum += sff->IDL; 
	chsum += len;

	for(i = 0; i < len - 1; i++)
		chsum += sff->data[i];

	return chsum;
}

DeviceInfo *GetECOMDevices()
{
	//structure that will be used to retrieve information about each device
	DeviceInfo deviceInfoStruct;
	//Obtain a search handle that can be used to retrieve ALL connected ECOM devices.
	DEV_SEARCH_HANDLE searchHandle = StartDeviceSearch(FIND_ALL);

	int deviceCount = 0;

	DeviceInfo *toret = (DeviceInfo *) malloc(sizeof(DeviceInfo) * 10);
	memset(toret, 0, sizeof(DeviceInfo)*10);

	//Check for errors
	if (searchHandle == NULL)
	{
		printf("Unexpected error allocating memory for device search\n");
		return toret;
	}
	//Now retrieve each attached device until there are no more left
	//When the searching is done, it will return ECI_NO_MORE_DEVICES

	while(FindNextDevice(searchHandle, &deviceInfoStruct) == ECI_NO_ERROR)
	{
		//Print the serial number of the found device
		printf("Device Found: %d\n", deviceInfoStruct.SerialNumber);
		memcpy((void *) &toret[deviceCount++], &deviceInfoStruct, sizeof(DeviceInfo));
	}
//	printf("Found %d devices\n", deviceCount);
	//Make sure to close the search handle to free up memory used.
	CloseDeviceSearch(searchHandle);
	return toret; //return the number of attached devices
}

int main(int argc, char *argv[])
{
	FILE *fp = NULL, *input_fp = NULL;
	char ch = '\0'; 
	char line[LINEMAX]; 
	SFFMessage *sff_msgs = NULL;  
	SFFMessage sff_send;
	SFFMessage *sff_sends;
	int input_lines = 0, cnt = 0, lc = 0, sff_cnt = 0, i = 0, queue_size = 0, line_len = 0, frame_cnt = 500000; 
	BYTE ReturnError = 0; 
	DeviceInfo *EcomDevices;
	int j = 0;
	long EndTime, StartTime;
	DWORD AcceptMask = 0, AcceptCode = 0; 
	unsigned short wid;
	
	//Toyota LKA turn wheel 5 degrees counter clockwise
	//char *static_cont_line = "IDH: 02, IDL: E4, Len: 05, Data: 81 05 00 80 F0";

	//Toyota Immobilizer makes car stop regardless of GAS 
	//char *static_cont_line = "IDH: 02, IDL: 83, Len: 07, Data: 61 00 E0 BE 8C 00 17";

	//acceleration pedal 
	char *static_cont_line = "IDH: 00, IDL: 37, Len: 07, Data: C9 17 58 14 29 00 B3";

	char *static_cont_lines[] = {	"IDH: 01, IDL: 27, Len: 08, Data: 68 10 00 08 87 3C BE 31",
									"IDH: 00, IDL: 37, Len: 07, Data: C2 13 52 03 AC 00 14",
									//"IDH: 01, IDL: 28, Len: 08, Data: 00 00 10 00 00 00 00 41",
									//"IDH: 01, IDL: 25, Len: 07, Data: 00 10 00 C0 D0 20 ED",
									//"IDH: 01, IDL: 28, Len: 08, Data: 00 00 10 00 00 00 00 41",
									0};

	//Set all the CAN IDs to be non-filtered, then set msgs of interest by flipping the bit
	memset(&CANID_11BIT, 0x0, sizeof(CANID_11BIT)); 

	//Toyota Update IDs
	//CANID_11BIT[0x07E0] = 1;
	//CANID_11BIT[0x07E8] = 1;
	//CANID_11BIT[0x07E2] = 1; 
	//CANID_11BIT[0x07EA] = 1;
	//CANID_11BIT[0x07DF] = 1;
	//CANID_11BIT[0x07E1] = 1;
	//CANID_11BIT[0x07E9] = 1;
	//CANID_11BIT[0x0720] = 1;
	//CANID_11BIT[0x0001] = 1;
	//CANID_11BIT[0x0002] = 1;
	//CANID_11BIT[0x0003] = 1;
	//CANID_11BIT[0x0004] = 1;
	//CANID_11BIT[0x0005] = 1;
	//CANID_11BIT[0x0006] = 1;
	//CANID_11BIT[0x0007] = 1;
	//CANID_11BIT[0x0008] = 1;
	//CANID_11BIT[0x0009] = 1;
	
	//Toyota Driving Support
	//CANID_11BIT[0x02E4] = 1;
	//CANID_11BIT[0x0283] = 1;
	//CANID_11BIT[0x0344] = 1;
	//CANID_11BIT[0x03A9] = 1;
	//CANID_11BIT[0x0689] = 1;
	//CANID_11BIT[0x04CB] = 1;

	//Toyota Speed Related IDs
	//CANID_11BIT[0x00B4] = 1;
	//CANID_11BIT[0x00B6] = 1;
	
	//Toyota PowerMgmt ECU
	//CANID_11BIT[0x0037] = 1;
	//CANID_11BIT[0x0039] = 1;
	//CANID_11BIT[0x00B0] = 1;
	//CANID_11BIT[0x00B2] = 1;
	//CANID_11BIT[0x0125] = 1;
	//CANID_11BIT[0x01C4] = 1;
	//CANID_11BIT[0x0244] = 1;
	//CANID_11BIT[0x0236] = 1;
	//CANID_11BIT[0x02C6] = 1;
	//CANID_11BIT[0x02CB] = 1;
	//CANID_11BIT[0x0348] = 1;
	//CANID_11BIT[0x03C8] = 1;
	//CANID_11BIT[0x03CB] = 1;
	//CANID_11BIT[0x03CA] = 1;
	//CANID_11BIT[0x03CF] = 1;

	EcomDevices = GetECOMDevices();

#pragma region OpenECOMDevices
	if (EcomDevices->SerialNumber == 0)
	{
		printf("Problem getting ECOM devices\n");
		goto epilog;
	}

	j=0;
	while ( (EcomDevices + j)->SerialNumber != 0){
		ULONG serial = (EcomDevices + j)->SerialNumber;
		HANDLE dh;
		BYTE baud = CAN_BAUD_500K;
		// special case for MS can bus 
		if (serial == MS_BUS_SERIAL){
			baud = CAN_BAUD_125K;
		}

//		serial = atoi(argv[1]);//CAM
		printf("Opening %d at %d\n", serial, baud);
		 
		dh = CANOpen(serial, baud, &ReturnError); 
		(EcomDevices + j)->DeviceHandle = dh;

		if (!dh || ReturnError != 0)
		{
			char ErrMsg[400];
			GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);  //ECOM Library call to get text describing error code
			printf("CANOpen failed with error message: ");
			printf(ErrMsg);
			goto epilog;
		} else {

			//Set ansychronous 
			ReturnError = CANSetupDevice(dh, CAN_CMD_TRANSMIT, CAN_PROPERTY_ASYNC); 
		}
		j++;
	}
#pragma endregion OpenECOMDevices

#pragma region contsend
	if(CONTSEND)
	{
		char *cont_line = static_cont_line;
		BYTE counter;
		HANDLE h;
		int time_to_send = 100000;

		if (argc >= 2){
			cont_line = argv[1];
		}

		if (argc >= 3){
			time_to_send = atoi(argv[2]);
		}

		memset(&sff_send, 0x0, sizeof(SFFMessage));
		DbgLineToSFF(cont_line, &sff_send); 

		// Get handle figured out
		i=0;
		//printf("handle %d\n", h);
		while ( (EcomDevices + i)->DeviceHandle ){
			if( (EcomDevices + i)->SerialNumber == MS_BUS_SERIAL){
				//printf("Found ms\n");
				if( sff_send.baud == CAN_BAUD_125K){
					//printf("That guy has 125k\n");
					h = (EcomDevices + i)->DeviceHandle;
					break;
				} else {
					//printf("ms guy doesn't have 125k\n");
				}
			} else {
				//printf("Found hs\n");
				h = (EcomDevices + i)->DeviceHandle;
			}
			i++;
		}
		//printf("handle %d\n", h);
		EndTime = clock() + ENDTIME; 

		//set auto hardware recv after send
		sff_send.options |= 1 << 4; 

		//now that we've collected all the msgs, lets send them along
		i = 0;
		while (clock() < EndTime)
		{
			//if(i % 100 == 1)
			//	printf(".");

			//send a message
			ReturnError = CANTransmitMessage(h, &sff_send); 
			if(ReturnError==0){
				i++;
			}

			//change increment the first byte and ensure its between a range
			if(LOOPER)
			{ 
				//00B4 speed counter
				//sff_send.data[4]++ & 0xFF; 
				
				//attempt for cruise control
				//sff_send.data[0]++;
				//sff_send.data[0] &= 0x7F;

				//for LKA steering
				//sff_send.data[0]++ & 0xFF; 
				//sff_send.data[0] |= 0x80; 
				
				//sff_send.data[sff_send.DataLength-1] = SFFChecksum(&sff_send);
				//PrintSFF(&sff_send, NULL);
			}
			
		}
	}
	printf("Did %d packets\n", i);
#pragma endregion contsend

#pragma region megaball
	if(MEGABALL)
	{
		char *cont_line;
		HANDLE h;
		int nummessages=0;
		cont_line = static_cont_lines[0];
		while(cont_line){
			nummessages++;
			cont_line = static_cont_lines[nummessages];
		}

		printf("Found %d messages to play\n", nummessages);

		sff_sends = (SFFMessage *) malloc(nummessages * sizeof(SFFMessage));
		for(i=0; i<nummessages; i++)
		{
			memset(&sff_sends[i], 0x0, sizeof(SFFMessage));
			DbgLineToSFF(static_cont_lines[i], &sff_sends[i]); 
		}

		// Get handle figured out
		i=0;
		while ( (EcomDevices + i)->DeviceHandle ){
			if( (EcomDevices + i)->SerialNumber == MS_BUS_SERIAL){
				if( sff_sends[0].baud == CAN_BAUD_125K){
					h = (EcomDevices + i)->DeviceHandle;
					break;
				}
			} else {
				h = (EcomDevices + i)->DeviceHandle;
			}
			i++;
		}

		EndTime = clock() + ENDTIME; 

		//set auto hardware recv after send
		sff_send.options |= 1 << 4; 

		i=0;
		while (clock() < EndTime)
		{
			int j;
			for(j=0;j<nummessages;j++){
				ReturnError = CANTransmitMessage(h, &sff_sends[j]); 
			}
		}
	}
#pragma endregion megaball

#pragma region inputmode
	if(INPUTMODE)
	{
		HANDLE hs_handle, ms_handle;

		if(argc > 1) 
			input_fp = fopen(argv[1], "r");
		else
			input_fp = fopen(INFILE, "r");

		if(!input_fp)
		{
			printf("Error opening %s\n", INFILE);
			return -1; 
		}

		//count the lines
		while(ch != EOF) 
		{
			ch = getc(input_fp); 
			line_len++; 
			if(ch == '\n')
			{
				if(line_len > 1)
					input_lines++; 
				line_len = 0; 
			}
		}
		fclose(input_fp); 

		printf("Number of input lines: %d\n", input_lines);

		sff_msgs = (SFFMessage*)malloc(sizeof(SFFMessage) * input_lines); 
		if(sff_msgs == NULL)
		{
			printf("Error allocating SFFMessage buffer\n");
			goto epilog;
		}
		memset(sff_msgs, 0x0, sizeof(SFFMessage) * input_lines); 

		if(argc > 1)
			input_fp = fopen(argv[1], "r");
		else
			input_fp = fopen(INFILE, "r");

		if(!input_fp)
		{
			printf("Error opening %s\n", INFILE);
			goto epilog; 
		}

		memset(&line, 0x0, LINEMAX); 
		ch = NULL; 
		while(ch != EOF) 
		{
			ch = getc(input_fp); 
			if(ch == '\n')
			{
				if(cnt + 1 >= LINEMAX)
				{
					printf("Line too long\n");
					return -1;
				}

				lc++; 
				line[cnt+1] = '\0'; 
				//printf("Line %d: %s\n", lc, line);
 
				if(strlen(line) > 1)
				{
					DbgLineToSFF(line, &(sff_msgs[sff_cnt])); 
					sff_cnt++;
				}
				memset(&line, 0x0, LINEMAX); 
				cnt = 0; 

			}
			else
			{
				if(cnt >= LINEMAX)
				{
					printf("Line too long\n");
					return -1;
				}

				line[cnt] = ch; 
				cnt++;
			}
		}

		//now that we've collected all the msgs, lets send them along


		// Get handles figured out
		i=0;
		while ( (EcomDevices + i)->DeviceHandle ){
			if( (EcomDevices + i)->SerialNumber == MS_BUS_SERIAL){
				ms_handle = (EcomDevices + i)->DeviceHandle;
			} else {
				hs_handle = (EcomDevices + i)->DeviceHandle;
			}
			i++;
		}

		EndTime = clock() + ENDTIME; 

		//set auto hardware recv after send
		sff_send.options |= 1 << 4; 

		i=0;
		while (clock() < EndTime)
		{
			for(i = 0; i < input_lines; i++) 
			{
				int k;
				HANDLE h = hs_handle;
				//printf("Sending SFFMessage[%d]\n", i); 

				//set hardware based self receiption
				sff_msgs[i].options |= 1 << 4; 

				PrintSFF(&(sff_msgs[i]), NULL);

				if (sff_msgs[i].baud == CAN_BAUD_125K){
					h = ms_handle;
				}

				ReturnError = CANTransmitMessage(h, &(sff_msgs[i])); 
			}
		}
		
	}
#pragma endregion inputmode

#pragma region SLOWINPUT
	if(SLOWINPUT)
	{
		HANDLE hs_handle, ms_handle;

		if(argc > 1) 
			input_fp = fopen(argv[1], "r");
		else
			input_fp = fopen(INFILE, "r");

		if(!input_fp)
		{
			printf("Error opening %s\n", INFILE);
			return -1; 
		}

		//count the lines
		while(ch != EOF) 
		{
			ch = getc(input_fp); 
			line_len++; 
			if(ch == '\n')
			{
				if(line_len > 1)
					input_lines++; 
				line_len = 0; 
			}
		}
		fclose(input_fp); 

		printf("Number of input lines: %d\n", input_lines);

		sff_msgs = (SFFMessage*)malloc(sizeof(SFFMessage) * input_lines); 
		if(sff_msgs == NULL)
		{
			printf("Error allocating SFFMessage buffer\n");
			goto epilog;
		}
		memset(sff_msgs, 0x0, sizeof(SFFMessage) * input_lines); 

		if(argc > 1)
			input_fp = fopen(argv[1], "r");
		else
			input_fp = fopen(INFILE, "r");

		if(!input_fp)
		{
			printf("Error opening %s\n", INFILE);
			goto epilog; 
		}

		memset(&line, 0x0, LINEMAX); 
		ch = NULL; 
		while(ch != EOF) 
		{
			ch = getc(input_fp); 
			if(ch == '\n')
			{
				if(cnt + 1 >= LINEMAX)
				{
					printf("Line too long\n");
					return -1;
				}

				lc++; 
				line[cnt+1] = '\0'; 
				//printf("Line %d: %s\n", lc, line);
 
				if(strlen(line) > 1)
				{
					DbgLineToSFF(line, &(sff_msgs[sff_cnt])); 
					sff_cnt++;
				}
				memset(&line, 0x0, LINEMAX); 
				cnt = 0; 

			}
			else
			{
				if(cnt >= LINEMAX)
				{
					printf("Line too long\n");
					return -1;
				}

				line[cnt] = ch; 
				cnt++;
			}
		}

		//now that we've collected all the msgs, lets send them along


		// Get handles figured out
		i=0;
		while ( (EcomDevices + i)->DeviceHandle ){
			if( (EcomDevices + i)->SerialNumber == MS_BUS_SERIAL){
				ms_handle = (EcomDevices + i)->DeviceHandle;
			} else {
				hs_handle = (EcomDevices + i)->DeviceHandle;
			}
			i++;
		}

		EndTime = clock() + ENDTIME; 

		//set auto hardware recv after send
		sff_send.options |= 1 << 4; 

		i=0;
		while (clock() < EndTime)
		{

			StartTime = clock();

			for(i = 0; i < input_lines; i++) 
			{
				int k;
				HANDLE h = hs_handle;
				//printf("Sending SFFMessage[%d]\n", i); 
				//printf("%d\n", sff_msgs[i].TimeStamp);

				//set hardware based self receiption
				sff_msgs[i].options |= 1 << 4; 

				PrintSFF(&(sff_msgs[i]), NULL);

				if (sff_msgs[i].baud == CAN_BAUD_125K){
					h = ms_handle;
				}

				// message timestamp is measured in .1 ms.
				while( 10 * (clock() - StartTime) < sff_msgs[i].TimeStamp){
					ReturnError = CANTransmitMessage(h, &(sff_msgs[i])); 
				}

				if(ReturnError != 0)
				{
						//char ErrMsg[400];
						//GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
						//printf("CANReceiveMessage failed when sending msg[%d]: ", i);
						//printf(ErrMsg);
						//goto epilog;
				}

			}
		}
		
	}
#pragma endregion slowinput

#pragma region outputmode
	EndTime = clock() + ENDTIME; 
	if(OUTPUTMODE)
	{
		if(argc > 1)
			fp = fopen(argv[1], "w");
		else
			fp = fopen(OUTFILE, "w");

		if(!fp)
		{
			printf("Error opening %s\n", OUTFILE);
			return -1;
		}

		//Just a simple example, this will display all received 11-bit CAN packets for 10 seconds	 
		printf("Starting to recv CAN traffic\n");

		while (clock() < EndTime)
		{
			//SFFMessage RxMessage;  //This structure will hold the incoming CAN message
			SFFMessage RxMessage; 
			EFFMessage EffMsg; 
			int j = 0;	

			while( (EcomDevices + j)->SerialNumber != 0){
				HANDLE dh = (EcomDevices + j)->DeviceHandle;
				int baud = (EcomDevices+j)->SerialNumber == MS_BUS_SERIAL ? CAN_BAUD_125K: CAN_BAUD_500K;

				ReturnError = CANReceiveMessage(dh, &RxMessage);
				RxMessage.baud = baud;
				if (ReturnError == CAN_NO_RX_MESSAGES)
				{
					Sleep(1); //wait for messages since there are none yet
				}
				else if (ReturnError != 0)
				{
					//We got an error message (besides CAN_NO_RX_MESSAGES), so return and exit
					char ErrMsg[400];
					GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
					printf("CANReceiveMessage failed with error message: ");
					printf(ErrMsg);
					goto epilog;
				}
				else  //ReturnError == 0, which means we successfully received a message
				{
					if(FILTERMODE) 
					{
						if(FILTERMODE == 1)
						{
							if(RxMessage.IDH == FILTER_IDH && RxMessage.IDL == FILTER_IDL) 
								PrintSFF(&RxMessage, fp);
						}
						else if(FILTERMODE == 2)
						{
							wid = (RxMessage.IDH << 8) | RxMessage.IDL; 
							if(CANID_11BIT[wid] == 1)
								PrintSFF(&RxMessage, fp);	
						}
						else if(FILTERMODE ==3)
						{
							if(RxMessage.IDH == FILTER_IDH)
								PrintSFF(&RxMessage, fp);
						}
					}
					else
					{
						PrintSFF(&RxMessage, fp);
					}	 
				} // end reading 11 bit.
	

				/*
				** 29 bit stuff
				*/
				/*
				ReturnError = CANReceiveMessageEx(dh, &EffMsg); 
				if (ReturnError == CAN_NO_RX_MESSAGES)
				{
					printf("%d",j);
					Sleep(1); //wait for messages since there are none yet
				}
				else if (ReturnError != 0)
				{
					//We got an error message (besides CAN_NO_RX_MESSAGES), so return and exit
					char ErrMsg[400];
					GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
					printf("CANReceiveMessageEx failed with error message: ");
					printf(ErrMsg);
					return -1;
				}
				else  //ReturnError == 0, which means we successfully received a message
				{
					printf("29 bit, bitch!!!!!!!!!!!!!!!!!!!!!!!\n");
					PrintEFF(&EffMsg, fp); 
				}
				// end reading 29 bit
				*/
				j++;
			}
		}
	}
#pragma endregion outputmode

#pragma region ReadAndWrite
	if(READANDWRITE)
	{ 
		SFFMessage RxMessage; 
		unsigned short wheelbyte = 0;
		int num_times = 120;
		int diffs[] = {-10,-16,-24,-30,-40,-46,-54,-60,-70,-76,-84,-94,-100,-108,-114,-122,-130,-138,-146,-152,-160,-168,-176,-184,-192,-194};
		int end_diff = -194;
		unsigned int start = 0x4E6B; 
		unsigned int ts_diff = 312;
		unsigned int newposition;
		unsigned int timestamp;
		unsigned int index;
		HANDLE sendhandle;
		printf("Starting to recv CAN traffic\n");

		while (wheelbyte == 0)
		{
			//SFFMessage RxMessage;  //This structure will hold the incoming CAN message

			int j = 0;	
			while( (EcomDevices + j)->SerialNumber != 0){
				HANDLE dh = (EcomDevices + j)->DeviceHandle;
				int baud = (EcomDevices+j)->SerialNumber == MS_BUS_SERIAL ? CAN_BAUD_125K: CAN_BAUD_500K;

				ReturnError = CANReceiveMessage(dh, &RxMessage);
				RxMessage.baud = baud;
				if (ReturnError == CAN_NO_RX_MESSAGES)
				{
					Sleep(1); //wait for messages since there are none yet
				}
				else if (ReturnError != 0)
				{
					//We got an error message (besides CAN_NO_RX_MESSAGES), so return and exit
					char ErrMsg[400];
					GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
					printf("CANReceiveMessage failed with error message: ");
					printf(ErrMsg);
					goto epilog;
				}
				else  //ReturnError == 0, which means we successfully received a message
				{
					if(RxMessage.IDH == 0x0 && RxMessage.IDL == 0x80) {
						PrintSFF(&RxMessage, NULL);
						wheelbyte = GetFirstDataShort(&RxMessage);
						printf("Got first byte of %x\n", wheelbyte);
						sendhandle = dh;
					}
				} // end reading 11 bit.
				j++;
			}
		}

		// got wheelbyte, now start sending packets
		newposition = wheelbyte;
		timestamp = 0;
		StartTime = clock();
		for (index = 0; index < sizeof(diffs); index++){
			CreateWheelPacket(&RxMessage, newposition, timestamp);
			PrintSFF(&RxMessage, NULL);
			while( 10 * (clock() - StartTime) < timestamp){
				ReturnError = CANTransmitMessage(sendhandle, &RxMessage); 
			}
			newposition += diffs[i];
			timestamp += ts_diff;
		}
		for (index = 0; index < num_times; index++){
			CreateWheelPacket(&RxMessage, newposition, timestamp);
			PrintSFF(&RxMessage, NULL);
			while( 10 * (clock() - StartTime) < timestamp){
				ReturnError = CANTransmitMessage(sendhandle, &RxMessage); 
			}
			newposition += end_diff;
			timestamp += ts_diff;
		}

	}
#pragma endregion ReadAndWrite


//	printf("Press enter to exit..");
//	getchar();

epilog:
	//Now we are all done, so clean up by closing the ECOM
	if(fp)
		fclose(fp);

	if(input_fp)
		fclose(input_fp);

	i=0;
	while ( (EcomDevices + i)->DeviceHandle ){
		CloseDevice( (EcomDevices + i)->DeviceHandle );
		i++;
	}

	if(sff_msgs)
		free(sff_msgs);

	return 0;
}