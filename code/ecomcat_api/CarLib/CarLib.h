#include "stdafx.h"

#define PARK 		1
#define DRIVE 		2
#define REVERSE 	3
#define NEUTRAL 	4
#define ENGINEBRAKE	5
#define LOW		6

#define BRAKE_ENGAGED		0
#define BRAKE_DISENGAGED 	1
#define BRAKE_LOCKED		2

#define AUTOPARK_ENABLED	0
#define AUTOPARK_DISABLED	1


class __declspec(dllexport) Car
{
protected:
	HANDLE ecom_device;
	unsigned short year; 

	unsigned short SPEED_WID;
	unsigned short RPM_WID;
	unsigned short BRAKE_PEDAL_WID; 
	unsigned short GAS_PEDAL_WID;
	unsigned short STEERING_ANGLE_WID; 
	unsigned short CURR_GEAR_WID;
	unsigned short AUTO_PARK_WID; 
	unsigned short AUTO_BRAKE_WID;

public:
	SFFMessage* get_single(unsigned short wid); 

	//getters
	virtual unsigned int GetSpeed() = 0; 
	virtual unsigned short GetRPM() = 0;
	virtual unsigned char GetBrakeState() = 0;
	virtual unsigned char GetGasPedalAngle() = 0; 
	virtual short GetSteeringAngle() = 0;
	virtual unsigned char GetCurrGear() = 0; 
	virtual unsigned char GetAutoPark() = 0; 
	virtual unsigned short GetAutoBrake() = 0;

	//setters
	virtual void SetAutoBrake(unsigned short pressure, unsigned int for_time) = 0; 
	virtual void SetSpeed(unsigned short KPH, unsigned int for_time) = 0; 
	virtual void SetSteeringAngle(short angle, unsigned int for_time) = 0; 
	virtual void SetRPM(unsigned short RPM, unsigned int for_time) = 0;
};

class __declspec(dllexport) ToyotaPrius : Car
{
public:
	ToyotaPrius();
	void AddChecksum(SFFMessage *sff); 

	//getters
	unsigned int GetSpeed(); 
	unsigned short GetRPM(); 
	unsigned char GetBrakeState(); 
	unsigned char GetGasPedalAngle();
	short GetSteeringAngle();
	unsigned char GetCurrGear(); 
	unsigned char GetAutoPark();
	unsigned short GetAutoBrake(); 

	//setters
	void SetAutoBrake(unsigned short pressure, unsigned int for_time); 
	void SetSpeed(unsigned short KPH, unsigned int for_time); 
	void SetSteeringAngle(short angle, unsigned int for_time);
	void SetRPM(unsigned short RPM, unsigned int for_time);

	//Car specific
	short GetServoAngle();
};

class __declspec(dllexport) FordEscape : Car
{
public:
	FordEscape();

	//getters
	unsigned int GetSpeed(); 
	unsigned short GetRPM(); 
	unsigned char GetBrakeState(); 
	unsigned char GetGasPedalAngle();
	short GetSteeringAngle();
	unsigned char GetCurrGear(); 
	unsigned char GetAutoPark();
	unsigned short GetAutoBrake(); 

	//setters
	void SetAutoBrake(unsigned short pressure, unsigned int for_time); 
	void SetSpeed(unsigned short KPH, unsigned int for_time); 
	void SetSteeringAngle(short angle, unsigned int for_time);
	void SetRPM(unsigned short RPM, unsigned int for_time);
};
