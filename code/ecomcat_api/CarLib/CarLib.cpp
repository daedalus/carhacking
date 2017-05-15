// CarLib.cpp : Defines the exported functions for the DLL application.
//

#include "stdafx.h"
#include "CarLib.h"

SFFMessage* Car::get_single(unsigned short wid)
{
	SFFMessage *sff;

	if(wid == 0x0)
	{
		fprintf(stderr, "WID: 0x0000 Not Valid\n");
		throw -1; 
	}

	sff = read_message_by_wid(ecom_device, wid);
	if(sff == NULL)
	{
		fprintf(stderr, "No Message Available %X\n", wid);
		throw -1; 
	}

	return sff; 
}

///<summary>Toyota Prius constructor. This must be called before any instance methods.</summary>
ToyotaPrius::ToyotaPrius()
{
	ecom_device = NULL; 

	ecom_device = open_device(CAN_BAUD_500K, 0);
	if(ecom_device == NULL) 
	{
		fprintf(stderr, "Invalid Ecom handle: <NULL>\n");
		throw -1; 
	}

	//CAN IDS
	SPEED_WID = 0x00B4; 
	RPM_WID = 0x01C4;
	BRAKE_PEDAL_WID = 0x0230;
	GAS_PEDAL_WID = 0x0245;
	STEERING_ANGLE_WID = 0x0025;  
	CURR_GEAR_WID = 0x0127; 
	AUTO_PARK_WID = 0x0266; 
	AUTO_BRAKE_WID = 0x0283; 

	year = 2010; 
}

///<summary>Ford Escape constructor. This must be called before any other instance methods.</summary>
FordEscape::FordEscape()
{
	ecom_device = NULL; 

	ecom_device = open_device(CAN_BAUD_500K, 0);
	if(ecom_device == NULL) 
	{
		fprintf(stderr, "Invalid Ecom handle: <NULL>\n");
		throw -1; 
	}

	//CAN IDS
	SPEED_WID = 0x0201; 
	RPM_WID = 0x0201;
	BRAKE_PEDAL_WID = 0x0200;
	GAS_PEDAL_WID = 0x0200;
	STEERING_ANGLE_WID = 0x0080; 
	CURR_GEAR_WID = 0x0230; 
	AUTO_PARK_WID = 0x0081; 
	AUTO_BRAKE_WID = 0x0000; 

	year = 2010; 
}

///<summary>A function that will add the byte-rounded checksum at the last slot in the sff->data[] array</summary>
void ToyotaPrius::AddChecksum(SFFMessage *sff)
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

	sff->data[sff->DataLength-1] = chsum; 
}

///<summary>Gets the current speed in MPH</summary>
unsigned int ToyotaPrius::GetSpeed()
{
	SFFMessage *sff; 
	unsigned short curr_speed; 

	sff = get_single(SPEED_WID); 

	curr_speed = (sff->data[5] << 8) | sff->data[6];
	curr_speed = (curr_speed * .0062); 
	
	return curr_speed;
}

///<summary>Gets the current RPM of the internal combustion engine</summary>
unsigned short ToyotaPrius::GetRPM()
{
	SFFMessage *sff; 
	unsigned short curr_rpm; 

	sff = get_single(RPM_WID); 

	curr_rpm = (sff->data[0] << 8) | sff->data[1]; 

	if(curr_rpm > 400)
		curr_rpm = curr_rpm - 400;
	else
		curr_rpm = 0; 

	return curr_rpm; 
}

///<summary>Get the current brake state. Engaged: 0x04. Locked: 0x0A. Dis-Engaged: 0x00</summary>
unsigned char ToyotaPrius::GetBrakeState()
{
	SFFMessage *sff;

	sff = get_single(BRAKE_PEDAL_WID);

	unsigned char brake = sff->data[3]; 

	switch(brake){
		case 0x04:
			return BRAKE_ENGAGED;
		case 0x0A:
			return BRAKE_LOCKED;
		case 0x00:
			return BRAKE_DISENGAGED;
	}
	return -1;
}

///<summary>Gets the current gas pedal angle. Un-depressed: 00. Fully-depressed: 0xC8</summary>
// between 00 and 100
unsigned char ToyotaPrius::GetGasPedalAngle()
{
	SFFMessage *sff;

	sff = get_single(GAS_PEDAL_WID);

	unsigned char pedal = sff->data[2]; 

	return pedal/2;
}

///<summary>Gets the steering wheel angle. Range: 0x157 (counter clockwise) - 0xEA9 (clockwise) [0x0000 is centered]</summary>
// between 100 to -100   TODO
short ToyotaPrius::GetSteeringAngle()
{
	SFFMessage *sff;
	signed short angle; 

	sff = get_single(STEERING_ANGLE_WID);

	angle = (sff->data[0] << 8) | sff->data[1]; 

	if (angle > 0x0800){
		angle = angle | 0xf000;
	}
	
	return 100 * angle / 0x157; 
}

///<summary>Gets the current gear of the car. Park: 0x00. Reverse: 0x10. Neutral: 0x20. Drive: 0x30. Engine Brake: 0x40</summary>
unsigned char ToyotaPrius::GetCurrGear()
{
	SFFMessage *sff;

	sff = get_single(CURR_GEAR_WID);
	unsigned char gear = sff->data[5] & 0xF0;
	switch(gear){
		case 0x00:
			return PARK;
		case 0x10:
			return REVERSE;
		case 0x20:
			return NEUTRAL;
		case 0x30:
			return DRIVE;
		case 0x40:
			return ENGINEBRAKE;
	}
	return -1;
}

///<summary>Gets the auto park state. Enabled: 0x30. Disabled: 0x10</summary>
unsigned char ToyotaPrius::GetAutoPark()
{
	SFFMessage *sff;

	sff = get_single(AUTO_PARK_WID);

	unsigned char autopark = (sff->data[0] & 0xF0); 

	if (autopark == 0x30){
		return AUTOPARK_ENABLED;
	}
	if (autopark == 0x10){
		return AUTOPARK_DISABLED;
	}
	return -1;
}

///<summary>Gets the brake pressure for the auto braking capability. Range 0xE000-0x0000 [Most-to-Least]</summary>
unsigned short ToyotaPrius::GetAutoBrake()
{
	SFFMessage *sff;
	unsigned short pressure; 

	sff = get_single(AUTO_BRAKE_WID);

	pressure = (sff->data[2] << 8) | sff->data[3]; 

	return pressure; 
}

///<summary>Sets the brake pressure for the auto braking capability. Range 0xE000-0x0000 [Most-to-Least]</summary>
void ToyotaPrius::SetAutoBrake(unsigned short pressure, unsigned int for_time) 
{
	SFFMessage sff; 

	memset(&sff, 0x0, sizeof(SFFMessage)); 

	sff.IDH = (AUTO_BRAKE_WID >> 8) & 0xFF; 
	sff.IDL = AUTO_BRAKE_WID & 0xFF; 

	sff.DataLength = 0x7; 

	sff.data[2] = (pressure >> 8) & 0xFF; 
	sff.data[3] = pressure & 0xFF; 
	sff.data[4] = 0x8C; 

	this->AddChecksum(&sff);

	PrintSFF(&sff, NULL); 

	write_message_cont(ecom_device, &sff, for_time);
}


///<summary>Sets the current speed in KPH</summary>
void ToyotaPrius::SetRPM(unsigned short RPM, unsigned int for_time) {
	// not implemented
}


///<summary>Sets the current speed in MPH</summary>
void ToyotaPrius::SetSpeed(unsigned short MPH, unsigned int for_time) 
{
	SFFMessage sff; 

	memset(&sff, 0x0, sizeof(SFFMessage)); 

	sff.IDH = (SPEED_WID >> 8) & 0xFF; 
	sff.IDL = SPEED_WID & 0xFF; 

	sff.DataLength = 0x8; 

	MPH = MPH * 161; 

	sff.data[5] = (MPH >> 8) & 0xFF; 
	sff.data[6] = MPH & 0xFF; 

	this->AddChecksum(&sff);

	PrintSFF(&sff, NULL); 

	write_message_cont(ecom_device, &sff, for_time);
}

short ToyotaPrius::GetServoAngle()
{
	SFFMessage *sff;
	short angle; 

	sff = get_single(AUTO_PARK_WID);

	angle = ((sff->data[0] & 0x0F) << 8) | sff->data[1]; 

	if (angle > 0x0800){
		angle = angle | 0xf000;
	}
	
	angle =  100 * angle / 0x157; 

	return angle; 
}

///<summary>Sets the steering wheel angle. Range: 0x157 (counter clockwise) - 0xEA9 (clockwise) [0x0000 is centered]</summary>
// Range 100 (counter clockwise) to -100 (clockwise). 0 is centered
void ToyotaPrius::SetSteeringAngle(short angle, unsigned int for_time)
{
	SFFMessage wheel_turn[2];
	SFFMessage *cur; 
	
	memset(&wheel_turn[0], 0x0, sizeof(SFFMessage)); 
	memset(&wheel_turn[1], 0x0, sizeof(SFFMessage)); 

	//set the gear in reverse 
	wheel_turn[0].IDH = (CURR_GEAR_WID >> 8) & 0xFF; 
	wheel_turn[0].IDL = CURR_GEAR_WID & 0xFF; 

	wheel_turn[0].DataLength = 0x08; 

	wheel_turn[0].data[0] = 0x68; 
	wheel_turn[0].data[1] = 0x10; 
	wheel_turn[0].data[3] = 0x0F; 
	wheel_turn[0].data[5] = 0x12;
	wheel_turn[0].data[6] = 0xAE; 

	this->AddChecksum(&wheel_turn[0]);

	//turn the wheel to the angle provided
	wheel_turn[1].IDH = (AUTO_PARK_WID >> 8) & 0xFF; 
	wheel_turn[1].IDL = AUTO_PARK_WID & 0xFF; 

	wheel_turn[1].DataLength = 0x08; 

	angle = (angle * 0x157 / 100 ) & 0xFFF; 

	wheel_turn[1].data[0] = 0x30 | ((angle >> 8) & 0xFF); 
	wheel_turn[1].data[1] = angle & 0xFF; 
	wheel_turn[1].data[2] = 0x10; 
	wheel_turn[1].data[3] = 0x01; 
	wheel_turn[1].data[6] = 0xAC; 

	this->AddChecksum(&wheel_turn[1]);

	PrintSFF(&wheel_turn[0], NULL); 
	PrintSFF(&wheel_turn[1], NULL); 

	cur = wheel_turn; 

	write_messages_cont(ecom_device, &cur, for_time); 
}

///<summary>Gets the current speed in MPH</summary>
unsigned int FordEscape::GetSpeed()
{
	SFFMessage *sff; 
	unsigned short curr_speed; 

	sff = get_single(SPEED_WID); 

	curr_speed = (sff->data[4] << 8) | sff->data[5];
	curr_speed = (curr_speed * .0065) - 65; 
	
	return curr_speed;
}

///<summary>Gets the current RPM of the internal combustion engine</summary>
unsigned short FordEscape::GetRPM()
{
	SFFMessage *sff; 
	unsigned short curr_rpm; 

	sff = get_single(RPM_WID); 

	curr_rpm = (sff->data[0] << 8) | sff->data[1]; 
	curr_rpm = (curr_rpm * .25) - 24; 	

	return curr_rpm; 
}

///<summary>Get the current brake state. Engaged: 0x01. Dis-Engaged: 0x00</summary>
unsigned char FordEscape::GetBrakeState()
{
	SFFMessage *sff;

	sff = get_single(BRAKE_PEDAL_WID);

	unsigned char brake = sff->data[6]; 
	
	if(brake == 0x1){
		return BRAKE_ENGAGED;
	}
	if(brake ==0x00){
		return BRAKE_DISENGAGED;
	}
	return -1;
}

///<summary>Gets the current gas pedal angle. Un-depressed: 00. Fully-depressed: 0x20</summary>
unsigned char FordEscape::GetGasPedalAngle()
{
	SFFMessage *sff;

	sff = get_single(GAS_PEDAL_WID);

	unsigned char gas = sff->data[7]; 

	return gas * 3;
}

///<summary>Gets the steering wheel angle. Range: 0x25C3 (counter clockwise) - 0x7661 (clockwise) [0x4D00 is centered]</summary>

short FordEscape::GetSteeringAngle()
{
	SFFMessage *sff;
	float angle; 
	unsigned short s_angle;

	sff = get_single(STEERING_ANGLE_WID);

	s_angle = (sff->data[0] << 8) | sff->data[1]; 
	
	angle = s_angle;
	angle = -(angle * .0097 - 193.68);

	return (short) angle; 
}

///<summary>Gets the current gear of the car. Park: 0x10. Reverse: 0x30. Neutral: 0x50. Drive: 0x70. Low: 0xC0</summary>
unsigned char FordEscape::GetCurrGear()
{
	SFFMessage *sff;

	sff = get_single(CURR_GEAR_WID);

	unsigned short gear = sff->data[7];
	switch(gear){
		case 0x10:
			return PARK;
		case 0x30:
			return REVERSE;
		case 0x50:
			return NEUTRAL;
		case 0x70:
			return DRIVE;
		case 0xc0:
			return LOW;
	}
	return -1;
}

///<summary>Gets the auto park state. Disabled: 0x00. Reduce Speed: 0x02. Searching: 0x04. Pull Forward: 0x08</summary>
unsigned char FordEscape::GetAutoPark()
{
	SFFMessage *sff;

	sff = get_single(AUTO_PARK_WID);

	unsigned char ap = sff->data[2]; 

	if (ap == 0){
		return AUTOPARK_DISABLED;
	}
	return AUTOPARK_ENABLED;
}

///<summary>XXX NOT IMPLEMENTED</summary>
unsigned short FordEscape::GetAutoBrake()
{
	fprintf(stderr, "FordEscape: AutoBrake Not Implemented");
	throw -1; 
}

///<summary>XXX NOT IMPLEMENTED</summary>
void FordEscape::SetAutoBrake(unsigned short pressure, unsigned int for_time) 
{
	fprintf(stderr, "FordEscape: AutoBrake Not Implemented");
	throw -1; 
}

///<summary>Sets the current speed in KPH</summary>
void FordEscape::SetSpeed(unsigned short MPH, unsigned int for_time) 
{
	SFFMessage sff; 

	memset(&sff, 0x0, sizeof(SFFMessage)); 

	sff.IDH = (SPEED_WID >> 8) & 0xFF; 
	sff.IDL = SPEED_WID & 0xFF; 

	sff.DataLength = 0x8; 

	MPH = 154 * (MPH + 67);

	sff.data[4] = (MPH >> 8) & 0xFF; 
	sff.data[5] = MPH & 0xFF; 

	PrintSFF(&sff, NULL); 

	write_message_cont(ecom_device, &sff, for_time);
}


///<summary>Sets the current RPM</summary>
void FordEscape::SetRPM(unsigned short RPM, unsigned int for_time) 
{
	SFFMessage sff; 

	memset(&sff, 0x0, sizeof(SFFMessage)); 

	sff.IDH = (SPEED_WID >> 8) & 0xFF; 
	sff.IDL = SPEED_WID & 0xFF; 

	sff.DataLength = 0x8; 

	RPM = 4 * (RPM + 24);

	sff.data[0] = (RPM >> 8) & 0xFF; 
	sff.data[1] = RPM & 0xFF; 

	PrintSFF(&sff, NULL); 

	write_message_cont(ecom_device, &sff, for_time);
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

void send_diagnostic_clear(HANDLE h){
	SFFMessage clear_dtc;
	// clear codes on electronic power steering...

	memset(&clear_dtc, 0x0, sizeof(SFFMessage)); 

	clear_dtc.IDH = 0x7; 
	clear_dtc.IDL = 0x30; 
	clear_dtc.DataLength = 0x8; 
	clear_dtc.data[0] = 0x03;
	clear_dtc.data[1] = 0x14;
	clear_dtc.data[2] = 0xff;
	write_message(h, &clear_dtc);
}

#define LINEMAX 100

int my_write_messages_from_file(HANDLE h, char *filename){
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


	SFFMessage faker;
	memset(&faker, 0x0, sizeof(SFFMessage));
	faker.DataLength = 8;
	faker.IDH = 0x02;
	faker.IDL = 0x01;
	memcpy(faker.data, "\x00\x00\x00\x00\x27\x10\x00\x00", 8);
	faker.TimeStamp = 0;
	faker.baud = 0;
	faker.options = 1<<4;

    //now that we've collected all the msgs, lets send them along
    StartTime = clock();
    for(i = 0; i < input_lines; i++)
    {
        printf("Sending SFFMessage[%d]\n", i);
        printf("%d\n", sff_msgs[i].TimeStamp);
        
        //set hardware based self receiption
        sff_msgs[i].options |= 1 << 4;
        
        PrintSFF(&(sff_msgs[i]), NULL);
//		PrintSFF(&faker, NULL);
                
		send_diagnostic_clear(h);

        // message timestamp is measured in .1 ms.  was 10
        while( 6 * (clock() - StartTime) < sff_msgs[i].TimeStamp){
            write_message(h, &(sff_msgs[i]));            
//			write_message(h, &faker);
		}
    }

	return input_lines;
    
}


// for now we ignore angle and for_time
//
void FordEscape::SetSteeringAngle(short angle, unsigned int for_time)
{
	SFFMessage *sff = (SFFMessage *) malloc(sizeof(SFFMessage)); 

	unsigned short wheelbyte = 0;
	int num_times = 120;
	int diffs[] = {-10,-16,-24,-30,-40,-46,-54,-60,-70,-76,-84,-94,-100,-108,-114,-122,-130,-138,-146,-152,-160,-168,-176,-184,-192,-194};
	int end_diff = -194; 
	unsigned int ts_diff = 312;
	unsigned int newposition;
	unsigned int timestamp;
	unsigned int index;

	send_diagnostic_clear(ecom_device);

	// hex version
	angle = 103.1 * (193.68 - angle);
	for_time *= 10;

	FILE *f = fopen("wheel.dat", "w");
	//
	// create file
	//

	// get where we are
	sff = get_single(STEERING_ANGLE_WID);
	wheelbyte = sff->data[1] + (sff->data[0] << 8);

	printf("current: %02X, future: %02X\n", wheelbyte, angle);
	if (wheelbyte < angle){   // turn clockwise
		newposition = wheelbyte;
		timestamp = 0;
		for (index = 0; (index < sizeof(diffs)/sizeof(int)) && (timestamp < for_time) && (newposition < angle); index++){
			CreateWheelPacket(sff, newposition, timestamp);
			PrintSFF(sff, f);
			newposition -= diffs[index];
			timestamp += ts_diff;
		}		
		for (index = 0; (timestamp < for_time) && (newposition < angle); index++){
			CreateWheelPacket(sff, newposition, timestamp);
			PrintSFF(sff, f);
			newposition -= end_diff;
			timestamp += ts_diff;
		}
	} else {				// turn counter-clockwise
		newposition = wheelbyte;
		timestamp = 0;
		for (index = 0; (index < sizeof(diffs)/sizeof(int)) && (timestamp < for_time) && (newposition > angle); index++){
			CreateWheelPacket(sff, newposition, timestamp);
			PrintSFF(sff, f);
			newposition += diffs[index];
			timestamp += ts_diff;
		}
		
		for (index = 0; (timestamp < for_time) && (newposition > angle); index++){
			CreateWheelPacket(sff, newposition, timestamp);
			PrintSFF(sff, f);
			newposition += end_diff;
			timestamp += ts_diff;
		}
	}

	while( timestamp < for_time){
		CreateWheelPacket(sff, newposition, timestamp);
		PrintSFF(sff, f);
		timestamp += ts_diff;
	}
	
	fclose(f);

	// write to can bus
	my_write_messages_from_file(ecom_device, "wheel.dat");

}



