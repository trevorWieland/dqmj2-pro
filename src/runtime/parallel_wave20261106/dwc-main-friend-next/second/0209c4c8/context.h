#include "error_types.h"
#include "string.h"
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef int BOOL;
typedef struct GTI2Socket*GT2Socket;typedef struct GTI2Connection*GT2Connection;
typedef unsigned char GT2Byte;typedef int GT2Bool;typedef int SOCKET;
typedef struct{void*connected,*received,*closed,*ping;}GT2ConnectionCallbacks;
typedef enum
{
	GT2Success,             
                            
	GT2OutOfMemory,         
	GT2Rejected,            
	GT2NetworkError,        
	GT2AddressError,        
	GT2DuplicateAddress,    
	GT2TimedOut,			
	GT2NegotiationError,	
	GT2InvalidConnection,	
	GT2InvalidMessage,		
	GT2SendFailed			
} GT2Result;
typedef struct{GT2Socket gt2Socket;GT2ConnectionCallbacks gt2Callbacks;int gt2SendBufSize,gt2RecvBufSize;u8 opaque28To43[16];u8 ownCloseFlag;}MainCoreConsumedPrefix;
typedef struct{MainCoreConsumedPrefix*control;int lastSocketError;}MainGlobalConsumedPrefix;
extern MainGlobalConsumedPrefix native_data_021d19e0;
#define stpDwcCnt native_data_021d19e0.control
#define stLastSocketError native_data_021d19e0.lastSocketError
#define DWC_Printf(...)
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define GT2True 1
#define GT2False 0
extern u32 native_fn_0209b368(u32);
#define DWCi_GetMathRand32 native_fn_0209b368
extern char*native_fn_020b5f38(u32,u16,char*);
#define gt2AddressToString native_fn_020b5f38
extern void native_fn_0209c4c8(GT2Socket);
#define DWCi_GT2SocketErrorCallback native_fn_0209c4c8
typedef void(*SocketErrorCallback)(GT2Socket);
typedef void(*ConnectAttemptCallback)(GT2Socket,GT2Connection,u32,u16,int,GT2Byte*,int);
typedef GT2Bool(*UnrecognizedCallback)(GT2Socket,u32,u16,GT2Byte*,int);
extern GT2Result native_fn_020b4330(GT2Socket*,const char*,int,int,SocketErrorCallback);
#define gt2CreateSocket native_fn_020b4330
extern GT2Result native_fn_0209bf8c(GT2Result);
#define DWCi_HandleGT2Error native_fn_0209bf8c
extern void native_fn_020b4374(GT2Socket,ConnectAttemptCallback);
#define gt2Listen native_fn_020b4374
extern void native_fn_0209ed44(GT2Socket,GT2Connection,u32,u16,int,GT2Byte*,int);
#define DWCi_GT2ConnectAttemptCallback native_fn_0209ed44
extern void native_fn_020b45a4(GT2Socket,UnrecognizedCallback);
#define gt2SetUnrecognizedMessageCallback native_fn_020b45a4
extern GT2Bool native_fn_0209eca4(GT2Socket,u32,u16,GT2Byte*,int);
#define DWCi_GT2UnrecognizedMessageCallback native_fn_0209eca4
extern void native_fn_020a41b4(GT2Connection,GT2Byte*,int,GT2Bool);
#define DWCi_RecvCallback native_fn_020a41b4
extern SOCKET native_fn_020b45a0(GT2Socket);
#define gt2GetSocketSOCKET native_fn_020b45a0
extern int native_fn_020a8c9c(SOCKET);
#define GOAGetLastError native_fn_020a8c9c
extern void native_fn_0209a9f8(DWCError,int);
#define DWCi_SetError native_fn_0209a9f8
struct in_addr{u32 s_addr;};
struct sockaddr_in{u8 sin_len,sin_family;u16 sin_port;struct in_addr sin_addr;};
struct sockaddr;
#define AF_INET 2
#define QR_MAGIC_1 0xfe
#define QR_MAGIC_2 0xfd
#define NATNEG_MAGIC_LEN 6
extern const unsigned char native_data_020e1738[];
#define NNMagicData native_data_020e1738
extern void native_fn_02008c14(u32,void*,u32);
static inline void MI_CpuClear32(void*dest,u32 bytes){native_fn_02008c14(0,dest,bytes);}
static inline u16 htons(u16 value){return (u16)((value<<8)|(value>>8));}
typedef struct{u8 opaque[16];void*qr2Obj;}MatchQr2ConsumedPrefix;
extern MatchQr2ConsumedPrefix*native_fn_020a3d70(void);
#define DWCi_GetMatchCnt native_fn_020a3d70
extern void native_fn_020b80a0(void*,char*,int,struct sockaddr*);
#define qr2_parse_query native_fn_020b80a0
extern void native_fn_020b70c8(char*,int,struct sockaddr_in*);
#define NNProcessData native_fn_020b70c8
typedef char gsi_char;
typedef struct{u8 keyID,isStr;u16 pad;char*keyStr;const void*value;}DWCGameMatchKeyData;
extern DWCGameMatchKeyData native_data_021d1ba8[];
#define stGameMatchKeys native_data_021d1ba8
#define DWC_QR2_GAME_KEY_START 100
#define DWC_ALLOCTYPE_BASE 4
extern u8 native_fn_020a2a9c(void);
#define DWCi_GetNewMatchKey native_fn_020a2a9c
extern void native_fn_0209aa64(int,void*,u32);
#define DWC_Free native_fn_0209aa64
extern void*native_fn_0209aa38(int,u32);
#define DWC_Alloc native_fn_0209aa38
extern void native_fn_0209f130(DWCError,int);
#define DWCi_StopMatching native_fn_0209f130
extern void native_fn_020b85d8(int,const char*);
#define qr2_register_key native_fn_020b85d8

void native_main_0209c4c8 (GT2Socket socket);
