#include <stdio.h>
#include "api_file.h"

#define IDH_STATE 1
#define IDL_STATE 2
#define LEN_STATE 3
#define DAT_STATE 4
#define TS_STATE  5
#define END_STATE 6

#define LINEMAX 100

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

///<summary>Takes a ASCII character debug line and converts it to a SFFMessage structure. See ecommlib.h for more details</summary>
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

///<summary>Prints a SFFMessage type to standard output and write it out to a file if fp is non-NULL</summary>
void PrintSFF(SFFMessage *sff, FILE *fp)
{
	int i = 0;

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

void FixChecksum(SFFMessage *sff)
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

	sff->data[len-1] = chsum;
}

///<summary>Opens an Ecom device. See ecommlib.h for baud values (Normally CAN_BAUD_500K). Serial can be null if only one device. Otherwise it should be the serial number of the device.</summary>
HANDLE open_device(unsigned int baud, unsigned int serial){

    HANDLE dh;
	BYTE ReturnError = 0;

    dh = CANOpen(serial, baud, &ReturnError);

    if (!dh || ReturnError != 0)
    {
        char ErrMsg[400];
        GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);  //ECOM Library call to get text describing error code
        printf("CANOpen failed with error message: ");
        printf(ErrMsg);
        return NULL;
    }
    ReturnError = CANSetupDevice(dh, CAN_CMD_TRANSMIT, CAN_PROPERTY_ASYNC);
	// seems this function always returns error...

    return dh;
}

///<summary>Closes the Ecom device handle.</summary>
int close_device(HANDLE h){
    return CloseDevice( h );
}

///<summary>Reads a single message from the Ecom device queue. The caller is responsible for freeing the SFFMessage.</summary>
SFFMessage *read_message(HANDLE h){
    BYTE ReturnError = CAN_NO_RX_MESSAGES;
    SFFMessage *ret = (SFFMessage *) malloc(sizeof(SFFMessage));

    while(ReturnError == CAN_NO_RX_MESSAGES){
        ReturnError = CANReceiveMessage(h, ret);
        Sleep(1);
    }

    if (ReturnError != 0)
    {
        //We got an error message (besides CAN_NO_RX_MESSAGES), so return and exit
        char ErrMsg[400];
        GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
        printf("CANReceiveMessage failed with error message: ");
        printf(ErrMsg);
        free(ret);
        return NULL;
    }
    else{
        return ret;
    }
}

///<summary>Reads a single message from the Ecom device queue by the specific CAN ID. The caller is responsible for freeing the SFFMessage.</summary>
SFFMessage *read_message_by_wid_get_ack_timeout(HANDLE h, unsigned short wid, BOOL tail_ack, unsigned int timeout)
{
    BYTE ReturnError = CAN_NO_RX_MESSAGES;
    SFFMessage *ret = (SFFMessage *) malloc(sizeof(SFFMessage));
	SFFMessage *saved_ret = NULL; 
    unsigned short read_wid = 0;
	long EndTime = clock() + timeout;
	BOOL seen_ack = FALSE;
	BOOL seen_tail_ack = FALSE;

	//printf("Options: Tail: %d\n", tail_ack); 

read_can_msg:
    while(ReturnError == CAN_NO_RX_MESSAGES || read_wid != wid){

		long CurTime = clock();
		if (CurTime > EndTime){
			free(ret);
			if(saved_ret)
				free(saved_ret); 
			return NULL;
		}

        ReturnError = CANReceiveMessage(h, ret);
        read_wid = (ret->IDH << 8) | ret->IDL;
        //Sleep(1);
    }
    
	//printf("Seen Ack: %d Tail Ack: %d\n", seen_ack, tail_ack);
	//printf("DBG->");
	//PrintSFF(ret, NULL);

    if (ReturnError != 0)
    {
        //We got an error message (besides CAN_NO_RX_MESSAGES), so return and exit
        char ErrMsg[400];
        GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
        printf("CANReceiveMessage failed with error message: ");
        printf(ErrMsg);
        free(ret);
        return NULL;
    }
    else
	{
		//printf("Data[0]: %02X Data[1]: %02X Data[2]: %02X\n", ret->data[0], ret->data[1], ret->data[2]);
		read_wid = 0x0000;
		
		if(seen_ack == FALSE)
		{
			PrintSFF(ret, NULL);
			memset(ret, 0x0, sizeof(SFFMessage));
			seen_ack = TRUE;
			EndTime = clock() + timeout;
			goto read_can_msg; 
		}

		if(tail_ack && seen_tail_ack == FALSE)
		{
			//we should have read the data so far
			saved_ret = (SFFMessage *) malloc(sizeof(SFFMessage));

			memcpy(saved_ret, ret, sizeof(SFFMessage)); 

			//PrintSFF(ret, NULL); 

			memset(ret, 0x0, sizeof(SFFMessage));

			seen_tail_ack = TRUE;

			EndTime = clock() + timeout;
			goto read_can_msg; 
		}
		
		//if we're looking for a tail ack and we've seen it
		//we can free the message used here and return the real data
		//otherwise just return our data
		if(tail_ack && seen_tail_ack)
		{
			free(ret);
			return saved_ret; 
		}
		else
		{
			return ret;
		}
    }
}

///<summary>Reads a single message from the Ecom device queue by the specific CAN ID. The caller is responsible for freeing the SFFMessage.</summary>
SFFMessage *read_message_by_wid(HANDLE h, unsigned short wid){
    BYTE ReturnError = CAN_NO_RX_MESSAGES;
    SFFMessage *ret = (SFFMessage *) malloc(sizeof(SFFMessage));
    unsigned short read_wid = 0;

    while(ReturnError == CAN_NO_RX_MESSAGES || read_wid != wid){
        ReturnError = CANReceiveMessage(h, ret);
        read_wid = (ret->IDH << 8) | ret->IDL;
        //Sleep(1);
    }
    
    if (ReturnError != 0)
    {
        //We got an error message (besides CAN_NO_RX_MESSAGES), so return and exit
        char ErrMsg[400];
        GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
        printf("CANReceiveMessage failed with error message: ");
        printf(ErrMsg);
        free(ret);
        return NULL;
    }
    else{
        return ret;
    }
}

SFFMessage *read_message_by_wid_with_timeout(HANDLE h, unsigned short wid, unsigned int timeout){

	BYTE ReturnError = CAN_NO_RX_MESSAGES;
    SFFMessage *ret = (SFFMessage *) malloc(sizeof(SFFMessage));
    unsigned short read_wid = 0;
	long EndTime = clock() + timeout;

    while(ReturnError == CAN_NO_RX_MESSAGES || read_wid != wid){
		long CurTime = clock();
		if (CurTime > EndTime){
			free(ret);
			return NULL;
		}
        ReturnError = CANReceiveMessage(h, ret);
        read_wid = (ret->IDH << 8) | ret->IDL;
        //Sleep(1);
    }
    
    if (ReturnError != 0)
    {
        //We got an error message (besides CAN_NO_RX_MESSAGES), so return and exit
        char ErrMsg[400];
        GetFriendlyErrorMessage(ReturnError, ErrMsg, 400);
        printf("CANReceiveMessage failed with error message: ");
        printf(ErrMsg);
        free(ret);
        return NULL;
    }
    else{
        return ret;
    }
}


///<summary>Writes a single message to the Ecom device.</summary>
int write_message(HANDLE h, SFFMessage *msg){
    msg->options |= 1 << 4;
	//PrintSFF(msg, NULL);
    return CANTransmitMessage(h, msg);
}

///<summary>Writes a single message to the Ecom device for the amount of time, in milliseconds, specified by 'for_time'</summary>
int write_message_cont(HANDLE h, SFFMessage *msg, unsigned int for_time){
	long EndTime = clock() + for_time;
    msg->options |= 1 << 4;
    while (clock() < EndTime)
    {
        CANTransmitMessage(h, msg);
    }
	return 0;
}

///<summary>Writes an array of messages to the Ecom device.</summary>
int write_messages(HANDLE h, SFFMessage **msgs){
    SFFMessage *cur_msg = msgs[0];
	while ((*cur_msg).DataLength > 0){
        (*cur_msg).options |= 1 << 4;
		CANTransmitMessage(h, cur_msg);
		cur_msg++;
    }
	return 0;
}

///<summary>Writes an array of messages to the Ecom device for the amount of time, in milliseconds, specified by 'for_time'</summary>
int write_messages_cont(HANDLE h, SFFMessage **msgs, unsigned int for_time){
	long EndTime = clock() + for_time;
    while (clock() < EndTime)
    {
        SFFMessage *cur_msg = msgs[0];
		while ( (*cur_msg).DataLength > 0 ){
            (*cur_msg).options |= 1 << 4;
            CANTransmitMessage(h, cur_msg);
            cur_msg++;
        }
    }
	return 0;
}

///<summary>Writes individual CAN messages to the Ecom device by reading each debug line in 'filename'</summary>
int write_messages_from_file(HANDLE h, char *filename){
    char ch = '\0';
    FILE *input_fp = fopen(filename, "r");
	SFFMessage *sff_msgs = NULL;
    unsigned int line_len = 0, input_lines = 0, lc = 0, i, cnt = 0, sff_cnt = 0;
	char line[LINEMAX]; 
    long StartTime;

    if(!input_fp)
    {
        printf("Error opening %s\n", filename);
        return 0;
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
        return -1;
    }
    memset(sff_msgs, 0x0, sizeof(SFFMessage) * input_lines);

    input_fp = fopen(filename, "r");

    memset(&line, 0x0, LINEMAX);
    ch = (char ) NULL;
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
    StartTime = clock();
    for(i = 0; i < input_lines; i++)
    {
//        printf("Sending SFFMessage[%d]\n", i);
//        printf("%d\n", sff_msgs[i].TimeStamp);
        
        //set hardware based self receiption
        sff_msgs[i].options |= 1 << 4;
        
        PrintSFF(&(sff_msgs[i]), NULL);
                
        // message timestamp is measured in .1 ms.
        while( 10 * (clock() - StartTime) < sff_msgs[i].TimeStamp){
            CANTransmitMessage(h, &(sff_msgs[i]));            
        }
    }

	return input_lines;
    
}

