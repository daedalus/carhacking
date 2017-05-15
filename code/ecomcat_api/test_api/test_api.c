// test_api.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "..\ecomcat_api\api_file.h"

int _tmain(int argc, _TCHAR* argv[])
{
	HANDLE h = open_device(CAN_BAUD_500K,0);
	SFFMessage *msg = NULL; 
	int num_network = 0; 

	while(1)
	{
		num_network = GetQueueSize(h, CAN_GET_SFF_SIZE);
		printf("%d\n", num_network); 
		msg = read_message(h); 
	}
	
//	SFFMessage sff[4];
//	SFFMessage *cur = sff;
//
//	memset(sff, 0, 4 * sizeof(SFFMessage));
//
//	DbgLineToSFF("IDH: 01, IDL: 67, Len: 08, Data: 00 60 00 00 00 00 00 69", cur++);
//	DbgLineToSFF("IDH: 01, IDL: 68, Len: 08, Data: 00 60 00 00 00 00 00 00", cur++);
//	DbgLineToSFF("IDH: 01, IDL: 69, Len: 08, Data: 41 41 41 41 41 41 41 41", cur++);
//
//	cur = sff;
////	write_messages(h, &cur);
////	PrintSFF(&sff[2], NULL);
//	cur = read_message(h);
////	cur = read_message_by_wid(h, 0x80);
//	PrintSFF(cur, NULL);
//
////	write_message(h, cur);
////	write_messages_from_file(h, "..\\test.dat");
//
//	close_device(h);

	return 0;
}

