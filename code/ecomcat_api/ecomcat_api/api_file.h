#include <stdio.h>
#include <time.h>
#include <string.h>
#include "ecommlib.h"


// open/close device
__declspec(dllexport) HANDLE open_device(unsigned int baud, unsigned int serial);
__declspec(dllexport) int close_device(HANDLE h);

// read messages
__declspec(dllexport) SFFMessage *read_message(HANDLE h);
__declspec(dllexport) SFFMessage *read_message_by_wid(HANDLE h, unsigned short wid);
__declspec(dllexport) SFFMessage *read_message_by_wid_get_ack_timeout(HANDLE h, unsigned short wid, BOOL tail_ack, unsigned int timeout);
__declspec(dllexport) SFFMessage *read_message_by_wid_with_timeout(HANDLE h, unsigned short wid, unsigned int timeout);

// write a single message
__declspec(dllexport) int write_message(HANDLE h, SFFMessage *msg);
__declspec(dllexport) int write_message_cont(HANDLE h, SFFMessage *msg, unsigned int for_time);

// try to write many messages, all may not be written due to speed of transit...
__declspec(dllexport) int write_messages(HANDLE h, SFFMessage **msgs);
__declspec(dllexport) int write_messages_cont(HANDLE h, SFFMessage **msgs, unsigned int for_time);

// read/write ISO 15765 data
__declspec(dllexport) char *read_15765_data(HANDLE h, unsigned short wid, unsigned int *len);
__declspec(dllexport) int write_15765_data(HANDLE h, unsigned short wid, char *data, unsigned int len);

// utility functions
__declspec(dllexport) void PrintSFF(SFFMessage *sff, FILE *fp);
__declspec(dllexport) int DbgLineToSFF(char *line, SFFMessage *sff);
__declspec(dllexport) int write_messages_from_file(HANDLE h, char *filename);
__declspec(dllexport) BYTE SFFChecksum(SFFMessage *sff);
__declspec(dllexport) BYTE FixChecksum(SFFMessage *sff);
