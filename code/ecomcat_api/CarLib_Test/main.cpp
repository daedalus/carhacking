#include "..\CarLib\CarLib.h"
#include <stdio.h>

int main(int argc, char *argv[])
{
	int i = 0;
//	ToyotaPrius *tp = new ToyotaPrius(); 
	//tp->SetAutoBrake(0xE0FF, 10000); 
	//tp->SetSpeed(20, 10000); 
	//tp->SetSteeringAngle(-100, 100000); 

	//printf("Steering Angle: %04X\n", tp->GetSteeringAngle()); 
	

	FordEscape *fe = new FordEscape();
//	fe->SetSpeed(60, 2000);
//	fe->SetRPM(4000, 2000);

	fe->SetSteeringAngle(atoi(argv[1]),atoi(argv[2]));
	 
	printf("Steering Angle: %d\n", fe->GetSteeringAngle());
	printf("Speed: %d\n", fe->GetSpeed()); 
	printf("RPM: %d\n", fe->GetRPM()); 
	printf("Brake: %d\n", fe->GetBrakeState()); 
	printf("Gas: %d\n", fe->GetGasPedalAngle());
	printf("Gear: %d\n", fe->GetCurrGear()); 
	printf("Autopark: %d\n", fe->GetAutoPark());

	return 0;
}