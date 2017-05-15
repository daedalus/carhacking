#ifndef __ECI_DLL_INCLUDE_FILE__
#define __ECI_DLL_INCLUDE_FILE__

#include <windows.h>
typedef void * HANDLE;
#define DEV_SEARCH_HANDLE	HANDLE

//Error Return Values
//Note that if CANTransmit() or CANTransmitEx() returns
//an error code other than one defined below that it
//is returning the Error Code Capture Register from the SJA1000
//CAN controller.  These error codes are explained in
//Section 5.2.3 of the SJA1000 Application Note AN97076
//and Section 6.4.9 of SJA1000 Data-Sheet
#define ERR_COULD_NOT_START_CAN				0xFF //failed to send commend to start CAN controller
#define ERR_COULD_NOT_ENUMERATE				0xFE //switching firmware and/or enumeration on USB bus failed
#define ERR_SERIAL_NUMBER_NOT_FOUND			0xFD //device with passed serial number not found
#define ERR_DEVICE_CLOSED					0xFC //the device at the received handle is closed
#define ERR_NO_DEVICES_ATTACHED				0xFB //No devices found (wait/unplug and try again)
#define ERR_INVALID_FIRMWARE				0xFA //multiple causes - possibly a bad DeviceHandle
#define ERR_ALREADY_OPEN_AS_CAN				0xF9 //device open already (existing device handle returned)
#define ERR_ALREADY_OPEN_AS_SERIAL			0xF8 //device open already (existing device handle returned)
#define ERR_NO_FREE_DEVICE					0xF7 //all attached devices are already open
#define ERR_INVALID_HANDLE					0xF6 //invalid device handle passed
#define ERR_CAN_COULD_NOT_READ_STATUS		0xF5 //Could not retrieve status from CAN device
#define ERR_USB_TX_FAILED					0xF4 //A failured occurred transfering on the USB bus to the device
#define ERR_USB_RX_FAILED					0xF3 //A failured occurred transfering on the USB bus to the device
#define ERR_USB_TX_LENGTH_MISMATCH			0xF2 //Unexpected error transfering on USB bus
#define ERR_CAN_TX_TIMEOUT					0xF1 //tx timeout occurred (msg may send on bus)
#define ERR_CAN_TX_ABORTED					0xF0 //synch. transfer aborted due to timeout
#define ERR_CAN_TX_ABORTED_UNEXPECTED		0xEF //synch. transfer unexpectedly aborted
#define ERR_NULL_DEVICE_HANDLE				0xEE //You passed a NULL device handle
#define ERR_INVALID_DEVICE_HANDLE			0xED
#define ERR_CAN_TX_BUFFER_FULL				0xEC //The async transfer buffer is full, wait and try again
#define ERR_CAN_RX_ZEROLENGTH_READ			0xEB //Reading the CAN bus returned a zero length msg (unexpected)
#define ERR_CAN_NOT_OPENED					0xEA //Device has not been opened as CAN
#define ERR_SERIAL_NOT_OPENED				0xE9 //Device has not been opened as Serial
#define ERR_COULD_NOT_START_THREAD			0xE8 //Thread could not be started
#define ERR_THREAD_STOP_TIMED_OUT			0xE7 //Thread did not stop in a reasonable amount of time
#define ERR_THREAD_ALREADY_RUNNING			0xE6
#define ERR_RXTHREAD_ALREADY_RUNNING		0xE5 //The receive MessageHandler thread is already running
#define ERR_CAN_INVALID_SETUP_PROPERTY		0xE4 //An invalid property was received by the CANSetupDevice() function
#define ERR_CAN_INVALID_SETUP_COMMAND		0xE3 //An invalid flag was received by the CANSetupDevice() function
#define ERR_COMMAND_FAILED					0xE2 //The command passed to SetupDevice failed
#define ERR_SERIAL_INVALID_BAUD				0xE1
#define ERR_DEVICE_UNPLUGGED				0xE0 //The device was physically removed from the CAN bus after being attached
#define ERR_ALREADY_OPEN					0xDF //The device is already open
#define ERR_NULL_DRIVER_HANDLE				0xDE //Could not retrieve a handle to the USB driver
#define ERR_SER_TX_BUFFER_FULL				0xDD
#define ERR_NULL_DEV_SEARCH_HANDLE			0xDC //A null device search handle was passed
#define ERR_INVALID_DEV_SEARCH_HANDLE		0xDB //An invalid search handle was passed
#define ERR_CONFIG_COMMAND_TIME_OUT			0xD9
#define ERR_NO_LONGER_SUPPORTED				0xD8 //This feature has been removed and is only supported for legacy purposes
#define ERR_NULL_PTR_PASSED					0xD7
#define ERR_INVALID_INPUT_BUFFER            0xD6 //Unexpected error, driver received invalid input buffer to IOCTL command
#define ERR_INVALID_INPUT_COMMAND           0xD5 //Unexpected error, driver received invalid input buffer to IOCTL command
#define ERR_ALREADY_OPEN_DIFFERENT_BAUD     0xD4 //CAN device is already opened by another application but at a different baud rate
#define ERR_ALREADY_OPEN_BY_PROCESS         0xD3 //Calling process already has this device open, or the unique ID is already in use
#define ERR_TOO_MANY_CONNECTS               0xD2 //Too many applications have connected to the driver (limit to 16)
#define ERR_ALREADY_OPEN_AS_EXCLUSIVE       0xD1 //Another application has opened the device for exclusive CAN access.
 
//Status Return Values
//The following return codes signify the error free
// completion of a function
#define ECI_NO_ERROR						0x00
#define CAN_NO_RX_MESSAGES					0x88
#define CAN_NO_ERROR_MESSAGES				0x89
#define ECI_NO_MORE_DEVICES					0x80   //No more devices are available from the FindNextDevice function

//ErrorMessage Control Bytes - these correspond to CAN error frames (and similar errors) that
//occurred on the bus. 
#define CAN_ERR_BUS					0x11 //A CAN Bus error has occurred (DataByte contains ErrorCaptureCode Register)
#define CAN_ERR_BUS_OFF_EVENT		0x12 //Bus off due to error
#define CAN_ERR_RESET_AFTER_BUS_OFF	0x13 //Error reseting SJA1000 after bus off event
#define CAN_ERR_RX_LIMIT_REACHED 	0x16 //The default rx error limit (96) has been reached
#define CAN_ERR_TX_LIMIT_REACHED 	0x17 //The default tx error limit (96) has been reached
#define CAN_BUS_BACK_ON_EVENT		0x18 //Bus has come back on after a bus off event due to errors
#define CAN_ARBITRATION_LOST		0x19 //Arbitration lost (DataByte contains location lost) see SJA1000 datasheet
#define CAN_ERR_PASSIVE				0x1A //SJA1000 has entered error passive mode
#define CAN_ERR_OVERRUN				0x1B //Embedded firmware has received a receive overrun
#define CAN_ERR_OVERRUN_PC			0x1C //PC driver received a receive overrun
#define ERR_ERROR_FIFO_OVERRUN		0x20 //Error buffer full - new errors will be lost
#define ERR_EFF_RX_FIFO_OVERRUN		0x21 //EFF Receive buffer full - messages will be lost
#define ERR_SFF_RX_FIFO_OVERRUN		0x22 //SFF Receive buffer full - messages will be lost

//Pass this instead of a serial number to CANOpen() or CANOpenFiltered() to find 
//the first CAN device attached to the USB bus that is not in use.
//You can then retrieve the serial number by passing the returned handle to GetDeviceInfo()
#define CAN_FIND_NEXT_FREE					0x00

//Setup Commands and valid properties for each used by CANSetupDevice()
#define CAN_CMD_TRANSMIT					0x00
	#define CAN_PROPERTY_ASYNC					0x00
	#define CAN_PROPERTY_SYNC					0x01

#define CAN_CMD_TIMESTAMPS					0x10
	#define CAN_PROPERTY_RECEIVE_TS			0x10
	#define CAN_PROPERTY_DONT_RECEIVE_TS	0x11

//Setup Properties for CANSetupDevice()
//The following constants are flags that are passed in the second parameter
//of the ReceiveCallback function
#define CAN_EFF_MESSAGES					0x30 //context byte is number of messages in EFF buffer
#define CAN_SFF_MESSAGES					0x31 //context byte is number of messages in SFF buffer 
#define CAN_ERR_MESSAGES					0x32 //context byte is number of messages in error buffer
#define SER_BYTES_RECEIVED					0x33 //context byte is number of messages in Serial receive buffer

//The following flags are passed to CANQueueSize to set which queue to check the size of
//for a device open as CAN
#define CAN_GET_EFF_SIZE		0  //Retrieve the current number of messages waiting to be received
#define CAN_GET_MAX_EFF_SIZE	1  //Get the max size of the EFF buffer  (fixed)
#define CAN_GET_SFF_SIZE		2  //...
#define CAN_GET_MAX_SFF_SIZE	3  //...  (fixed)
#define CAN_GET_ERROR_SIZE		4  //...
#define CAN_GET_MAX_ERROR_SIZE	5  //...  (fixed)
#define CAN_GET_TX_SIZE			6  //...
#define CAN_GET_MAX_TX_SIZE		7  //...  (fixed)

//for a device open as serial
#define SER_GET_RX_SIZE			8  //...
#define SER_GET_MAX_RX_SIZE		9  //...  (fixed)
#define SER_GET_TX_SIZE			10 //...
#define SER_GET_MAX_TX_SIZE		11 //...  (fixed)

//The following constants are flags that
//can be passed to the StartDeviceSearch function
#define FIND_OPEN							0x82
#define FIND_UNOPEN							0x83
#define FIND_ALL							0x87
#define FIND_NEXT							0x00

//The following are the pre-defined baud rates for CAN used by the CANOpen and CANOpenFiltered functions
#define CAN_BAUD_250K						0x00
#define CAN_BAUD_500K						0x01
#define CAN_BAUD_1MB						0x02
#define CAN_BAUD_125K						0x03

//The following are a few sample rates that are used by the CANOpenEx and CANOpenFilteredEx functions
//In order to set a custom CAN baud rate and bit-sample timings, pass CAN_BAUD_CUSTOM_TIMING
//as the baud rate and then appropriate values for the TimingRegisters variable 
//to the CANOpenEx and CANOpenFilteredEx functions.
//The TimingRegisters parameter corresponds to the SJA1000 CAN transceiver 
//Bus Timing Register 0 and 1 (BTR0 and BTR1) registers.  See the NXP SJA000 Transceiver 
//data sheet, Section 6.5 for more details.  A few common register settings are defined 
//below.  BTR0 is defined in the LSB and BTR1 in the MSB.
#define BUS_TIMING_REG_125K                 0x9C45
#define BUS_TIMING_REG_250K                 0x9C42
#define BUS_TIMING_REG_500K                 0x1841
#define BUS_TIMING_REG_1M                   0x1800

//OR this with the baud rate to enable listen-only mode using the CANOpen and CANOpenFiltered functions
#define CAN_LISTEN_ONLY						0x80

//OR the following bits with the BaudFlag variable in CANOpenEx and CANOpenFilteredEx for special function
#define CAN_LISTEN_ONLY_EX					0x80000000      //Enable listen-only mode
#define CAN_OPEN_EXCLUSIVE                  0x40000000      //Enable exclusive access mode, no other devices can open

//Serial Baud Rates
#define SERIAL_BAUD_2400	0
#define SERIAL_BAUD_4800	1
#define SERIAL_BAUD_9600	2
#define SERIAL_BAUD_19200	3
#define SERIAL_BAUD_28800	4
#define SERIAL_BAUD_38400	5
#define SERIAL_BAUD_57600	6


typedef struct
{
	DWORD	ID;		 
	BYTE	data[8];
	BYTE	options;  //BIT 6 = remote frame bit 
					  //set BIT 4 on transmissions for self reception
	BYTE	DataLength;
	DWORD	TimeStamp;  //Extending timestamp to support 4 byte TS mode... shouldnt hurt anything for older code using 2 byte mode
}	EFFMessage;

typedef struct
{
	BYTE	IDH;
	BYTE	IDL;
	BYTE	data[8];
	BYTE	options;  //BIT 6 = remote frame bit 
					  //set BIT 4 on transmissions for self reception
	BYTE	DataLength;
	DWORD	TimeStamp;  //Extending timestamp to support 4 byte TS mode... shouldnt hurt anything for older code using 2 byte mode
	BYTE	baud;
}	SFFMessage;

typedef struct
{
	ULONG	SerialNumber;       //Device serial number
	BYTE    CANOpen;	        //is device opened as CAN
	BYTE	SEROpen;	        //is device opened as Serial
	BYTE	_reserved;	        //legacy support - was used to indicate if message handler was running - now its always running
	BYTE	SyncCANTx;	        //always FALSE if returned by FindNextDevice
	HANDLE	DeviceHandle;       //NULL if structure returned by FindNextDevice - required b/c search is across all processes using the DLL and
						        //HANDLE will be invalid across multiple processes.  Each process must keep track of their open HANDLEs
    BYTE    OpenHandleCount;    //Number of handles that are open to this device (max is 16)    
    DWORD   CANTimingRegs;      //Timing registers currently in use (0xFFFFFFFF) is CAN is not open

	BYTE	reserved[5];
}	DeviceInfo;

typedef struct
{
	unsigned int ErrorFIFOSize;
	BYTE ErrorCode;
	BYTE ErrorData;
	double Timestamp;
	BYTE reserved[2];
}	ErrorMessage;

typedef BYTE (_stdcall *pMessageHandler)(HANDLE DeviceHandle, BYTE flag, DWORD flag_info, void* data);

//This will force all exported functions to be exported using the
//standard C format even when using a C++ compiler - make sure your
//compiler defines __cplusplus
#ifdef __cplusplus
extern "C"
{
#endif

//The following are functions that are exported by the DLL
DWORD  __stdcall GetLibraryVersion();
HANDLE __stdcall CANOpen(ULONG SerialNumber, BYTE baud, BYTE *error);
HANDLE __stdcall CANOpenEx(ULONG SerialNumber, DWORD BaudFlag, DWORD InstanceID, BYTE *error);
BYTE   __stdcall CANTransmitMessageEx(HANDLE DeviceHandle, EFFMessage *message);
BYTE   __stdcall CANTransmitMessage(HANDLE DeviceHandle, SFFMessage *message);
BYTE   __stdcall CANReceiveMessageEx(HANDLE DeviceHandle, EFFMessage *message);
BYTE   __stdcall CANReceiveMessage(HANDLE DeviceHandle, SFFMessage *message);
BYTE   __stdcall GetErrorMessage(HANDLE DeviceHandle, ErrorMessage *message);
BYTE   __stdcall GetDeviceInfo(HANDLE DeviceHandle, DeviceInfo *deviceInfo); 
BYTE   __stdcall CloseDevice(HANDLE DeviceHandle);
HANDLE __stdcall CANOpenFiltered(ULONG SerialNumber, BYTE baud, DWORD code, DWORD mask, BYTE *error);
HANDLE __stdcall CANOpenFilteredEx(ULONG SerialNumber, DWORD BaudFlag, DWORD InstanceID, DWORD code, DWORD mask, BYTE *error);
HANDLE __stdcall vbCANOpenFiltered(ULONG SerialNumber, BYTE baud, BYTE code1, BYTE code2, BYTE code3, BYTE code4, BYTE mask1, BYTE mask2, BYTE mask3, BYTE mask4, BYTE *error);
BYTE  __stdcall SetCallbackFunction(HANDLE DeviceHandle, pMessageHandler ReceiveCallback, void *data);
//CANStartMessageHandler is outdated and should no longer be used - instead use SetCallbackFunction 
BYTE   __stdcall CANStartMessageHandler(HANDLE DeviceHandle, pMessageHandler ReceiveCallback, void *data);
//CANStopMessageHandler is outdated and should no longer be used - it is equivalent to calling SetCallbackFunction with NULL parameters
BYTE   __stdcall CANStopMessageHandler(HANDLE DeviceHandle);
BYTE   __stdcall CANSetupDevice(HANDLE DeviceHandle, BYTE SetupCommand, BYTE SetupProperty);
HANDLE __stdcall SerialOpen(USHORT SerialNumber, BYTE baud, BYTE *error);
BYTE   __stdcall SerialWrite(HANDLE DeviceHandle, BYTE *buffer, LONG *length);
BYTE   __stdcall SerialRead(HANDLE DeviceHandle, BYTE *buffer, LONG *buffer_length);
int	  __stdcall GetQueueSize(HANDLE DeviceHandle, BYTE flag);
void	  __stdcall GetFriendlyErrorMessage(BYTE error, char *buffer, int buffer_size);

//Use the following functions to enumerate through devices
DEV_SEARCH_HANDLE __stdcall StartDeviceSearch(BYTE flag);
BYTE	  __stdcall CloseDeviceSearch(DEV_SEARCH_HANDLE searchHandle);
BYTE	  __stdcall FindNextDevice(DEV_SEARCH_HANDLE searchHandle, DeviceInfo *deviceInfo);

#ifdef __cplusplus
}  //end of extern "C"
#endif

#endif
