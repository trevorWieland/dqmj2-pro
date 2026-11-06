typedef struct{void*profileTable;int num,numBuddies;}GPIProfileList;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPProfile,GPEnum,GPIBool;
typedef struct{char*buffer;int size,len,pos;}GPIBuffer;
typedef struct{void(*callback)(GPConnection*,void*,void*);void*param;}GPICallback;
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;void*peerList,*callbackList,*lastCallback;GPIBuffer updateproBuffer,updateuiBuffer;void*transfers;u32 nextTransferID;int productID,namespaceID;char loginTicket[25];GPEnum quietModeFlags;u32 kaTransmit;}GPIConnection;
#define NULL ((void*)0)
#define GP_PARAMETER_ERROR 2
#define GP_NO_ERROR 0
#define GPI_DISCONNECTED 4
#define GP_REASON_LEN 1025
#define Error(c,r,s) do{native_fn_020b2c88(c,s);return r;}while(0)
void native_fn_020b2c88(GPConnection*,const char*);
char*native_fn_020b2a38(char*,const char*,u32);
GPResult native_fn_020ac6f4(GPConnection*,GPIBuffer*,const char*);
GPResult native_fn_020ac710(GPConnection*,GPIBuffer*,int);
#define strzcpy native_fn_020b2a38
#define gpiAppendStringToBuffer native_fn_020ac6f4
#define gpiAppendIntToBuffer native_fn_020ac710
extern const char native_data_020e0480[];
extern const char native_data_020e04b4[];
extern const char native_data_020e0470[];
extern const char native_data_020e04a8[];
extern const char native_data_020e0498[];
extern const char native_data_020e048c[];
extern const char native_data_020e0440[];
#define GP_STATUS_STRING_LEN 256
#define GP_LOCATION_STRING_LEN 256
int native_fn_0201d800(const char*,const char*);
#define strcmp native_fn_0201d800
extern const char native_data_020e04f4[];
extern const char native_data_020e050c[];
extern const char native_data_020e04dc[];
extern const char native_data_020e0518[];
extern const char native_data_020e0528[];

#define GPITrue 1
extern int native_data_021d23ec;
#define __GSIACResult native_data_021d23ec
#define GSIACAvailable 1
GPResult native_fn_020aa894(GPConnection*,int,int,int);
#define gpiInitialize native_fn_020aa894
GPResult native_fn_020aec50(GPConnection*,GPEnum,int);
#define gpiSetInfoi native_fn_020aec50
GPResult native_fn_020ac404(GPConnection*,GPProfile);
#define gpiAuthBuddyRequest native_fn_020ac404
typedef struct{int buddyIndex;GPEnum status;char*statusString,*locationString;u32 ip;u16 port;GPEnum quietModeFlags;}GPIBuddyStatus;
typedef struct{int buddyIndex;GPEnum statusState;char*richStatus,*gameType,*gameVariant,*gameMapName;u32 sessionFlags,buddyIp;u16 buddyPort;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;GPEnum quietModeFlags;int productId;void*extendedInfoKeys;}GPIBuddyStatusInfo;
typedef struct GPIProfile{int profileId,userId;GPIBuddyStatus*buddyStatus;GPIBuddyStatusInfo*buddyStatusInfo;void*cache;char*authSig;int requestCount;char*peerSig;int blocked,blockIndex,buddyOrBlockCache;}GPIProfile;
int native_fn_020b0a50(GPConnection*,int,GPIProfile**);int native_fn_020b0ca8(GPIProfile*);void native_fn_020b0b48(GPConnection*,GPIProfile*);void native_fn_020a929c(void*);
#define gpiGetProfile native_fn_020b0a50
#define gpiCanFreeProfile native_fn_020b0ca8
#define gpiRemoveProfile native_fn_020b0b48
#define gsifree native_fn_020a929c
typedef int GPErrorCode;
#define NOFILE 1
#define GPI_NUM_CALLBACKS 9
#define GPITrue 1
#define GPIFalse 0
#define GP_MEMORY_ERROR 1
#define freeclear(p) do{native_fn_020a929c(p);(p)=NULL;}while(0)
void*native_fn_020a927c(u32);void*native_fn_0201b208(void*,int,u32);GPIBool native_fn_020b08c8(GPConnection*);GPResult native_fn_020aa9b4(GPConnection*);void native_fn_020aa978(GPConnection*);void native_fn_020a8ef0(void);u32 native_fn_020a8ef8(void);void native_fn_0201d608(u32);
#define gsimalloc native_fn_020a927c
#define memset native_fn_0201b208
#define gpiInitProfiles native_fn_020b08c8
#define gpiReset native_fn_020aa9b4
#define gpiDestroy native_fn_020aa978
#define SocketStartUp native_fn_020a8ef0
#define current_time native_fn_020a8ef8
#define srand native_fn_0201d608

typedef u32 gsi_time;typedef struct GPIOperation_s GPIOperation;
#define GPI_READ_SIZE 2048
#define GP_NETWORK_ERROR 3
#define GP_SERVER_ERROR 4
#define GP_NETWORK 5
#define GP_CONNECTION_CLOSED 7
#define GP_FATAL 1
#define GPIFalse 0
#define GPI_PROFILE_DELETING 5
#define KEEPALIVE_TIMEOUT (60*2000)
#define assert(x) ((void)0)
#define gsDebugFormat(...) ((void)0)
#define max(a,b) ((a)>(b)?(a):(b))
#define CHECK_RESULT(expr) do{GPResult q=(expr);if(q!=GP_NO_ERROR)return q;}while(0)
#define CallbackFatalError(c,r,e,s) do{native_fn_020b2c6c(c,e,s);native_fn_020acbcc(c,r,1);return r;}while(0)
void native_fn_020ae834(GPConnection*,GPIBuffer*);
GPResult native_fn_020ac954(GPConnection*,int,GPIBuffer*,GPIBool*,GPIBool,char*);
GPResult native_fn_020ac880(GPConnection*,int,GPIBuffer*,int*,GPIBool*,char*);
void native_fn_020b2c6c(GPConnection*,int,const char*);void native_fn_020acbcc(GPConnection*,GPResult,GPEnum);
char*native_fn_0201d984(const char*,const char*);void*native_fn_020a928c(void*,u32);void*native_fn_0201b19c(void*,const void*,u32);void*native_fn_0201b1bc(void*,const void*,u32);
int native_fn_0201f274(const char*);GPIBool native_fn_020afb10(GPConnection*,GPIOperation**,int);GPResult native_fn_020afb68(GPConnection*,GPIOperation*,char*);
GPIBool native_fn_020b2a4c(GPConnection*,const char*,GPIBool);int native_fn_0201d914(const char*,const char*,u32);
GPResult native_fn_020aaf98(GPConnection*,const char*);GPIBool native_fn_020b2ae0(const char*,const char*,char*,int);GPResult native_fn_020ab96c(GPConnection*,const char*);
GPIBool native_fn_020afb40(GPConnection*);void native_fn_020a8f14(u32);
#define gpiAddLocalInfo native_fn_020ae834
#define gpiSendFromBuffer native_fn_020ac954
#define gpiRecvToBuffer native_fn_020ac880
#define gpiSetError native_fn_020b2c6c
#define gpiCallErrorCallback native_fn_020acbcc
#define strstr native_fn_0201d984
#define gsirealloc native_fn_020a928c
#define memcpy native_fn_0201b19c
#define memmove native_fn_0201b1bc
#define atoi native_fn_0201f274
#define gpiFindOperationByID native_fn_020afb10
#define gpiProcessOperation native_fn_020afb68
#define gpiCheckForError native_fn_020b2a4c
#define strncmp native_fn_0201d914
#define gpiProcessRecvBuddyMessage native_fn_020aaf98
#define gpiValueForKey native_fn_020b2ae0
#define gpiProcessRecvBuddyStatusInfo native_fn_020ab96c
#define gpiOperationsAreBlocking native_fn_020afb40
#define msleep native_fn_020a8f14
extern const char native_data_020e0548[];
extern const char native_data_020e054c[];
extern const char native_data_020e0578[];
extern const char native_data_020e0580[];
extern const char native_data_020e0590[];
extern const char native_data_020e0598[];
extern const char native_data_020e05a0[];
extern const char native_data_020e05a8[];
extern const char native_data_020e05b0[];
extern const char native_data_020e05b8[];
extern const char native_data_020e05e0[];

#undef strstr
#undef memcpy
#undef memmove
#undef strncmp
#undef atoi
#include "string.h"
#include "stdlib.h"

GPResult native_main_020aab70(GPConnection*);
