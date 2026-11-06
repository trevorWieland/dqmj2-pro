typedef struct{void*profileTable;int num,numBuddies,numBlocked;}GPIProfileList;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPProfile,GPEnum,GPIBool;
typedef struct{char*buffer;int size,len,pos;}GPIBuffer;
typedef struct{void(*callback)(GPConnection*,void*,void*);void*param;}GPICallback;
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;}GPIConnection;
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
