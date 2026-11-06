typedef struct{void*profileTable;int num,numBuddies,numBlocked;}GPIProfileList;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPProfile,GPEnum,GPIBool;
typedef struct{char*buffer;int size,len,pos;}GPIBuffer;
typedef struct{void(*callback)(GPConnection*,void*,void*);void*param;}GPICallback;
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;}GPIConnection;

#define NULL ((void*)0)
#define GP_NICK_LEN 31
#define GP_EMAIL_LEN 51
#define GP_NO_ERROR 0
#define GPIFalse 0
#define GPITrue 1
#define GSI_UNUSED(x) ((void)(x))
typedef struct{int buddyIndex;GPEnum status;char*statusString,*locationString;u32 ip;u16 port;GPEnum quietModeFlags;}GPIBuddyStatus;
typedef struct{int buddyIndex;GPEnum statusState;char*richStatus,*gameType,*gameVariant,*gameMapName;u32 sessionFlags,buddyIp;u16 buddyPort;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;GPEnum quietModeFlags;int productId;void*extendedInfoKeys;}GPIBuddyStatusInfo;
typedef struct GPIProfile{int profileId,userId;GPIBuddyStatus*buddyStatus;GPIBuddyStatusInfo*buddyStatusInfo;void*cache;char*authSig;int requestCount;char*peerSig;int blocked,blockIndex,buddyOrBlockCache;}GPIProfile;
typedef GPIBool(*gpiProfileMapFunc)(GPConnection*,GPIProfile*,void*);
typedef struct{char*nick,*email;GPIProfile**profile;GPIBool found;}GPIFindProfileByUserData;
typedef struct{GPConnection*connection;gpiProfileMapFunc func;void*data;}GPIProfileMapData;
typedef struct{int index;GPIProfile*profile;}GPIFindProfileData;
int native_fn_020a89f0(void*,const void*);void*native_fn_020a8ab0(void*,int(*)(void*,void*),void*);
GPIBool native_fn_020b0bd0(GPConnection*,gpiProfileMapFunc,void*);int native_fn_020b0bbc(void*,void*);
GPIBool native_fn_020b0b5c(GPConnection*,GPIProfile*,void*);GPIBool native_fn_020b0c00(GPConnection*,GPIProfile*,void*);
#define TableRemove native_fn_020a89f0
#define TableMapSafe2 native_fn_020a8ab0
#define gpiProfileMap native_fn_020b0bd0
#define gpiProfileMapCallback native_fn_020b0bbc
#define gpiCheckProfileForUser native_fn_020b0b5c
#define gpiCheckForBuddy native_fn_020b0c00

typedef u32 size_t;typedef int GPErrorCode,SOCKET;
#define GP_NETWORK_ERROR 3
#define GP_NETWORK 5
#define GP_PARSE 1
#define GP_SERVER_ERROR 4
#define GP_FATAL 1
#define GP_NON_FATAL 0
#define GP_PASSWORD_LEN 31
#define GP_XOR_SEED 0x79707367
#define GPI_CONNECTED 3
#define GPI_NOT_CONNECTED 0
#define GPI_DISCONNECTED 4
#define assert(x) ((void)0)
#define gsDebugFormat(...) ((void)0)
#define gsiSocketIsError(x) ((x)==-1)
#define CallbackFatalError(c,r,e,s) do{native_fn_020b2c6c(c,e,s);native_fn_020acbcc(c,r,1);return r;}while(0)
char*native_fn_0201d780(char*,const char*,u32);u32 native_fn_0201d69c(const char*);char*native_fn_0201d984(const char*,const char*);int native_fn_0201d914(const char*,const char*,u32);int native_fn_0201f274(const char*);
GPIBool native_fn_020b2ae0(const char*,const char*,char*,int);void native_fn_020acbcc(GPConnection*,GPResult,GPEnum);void native_fn_020b2c6c(GPConnection*,int,const char*);
int native_fn_020a8ca8(SOCKET,int*,int*,int*);void native_fn_020a8f68(u32);int native_fn_020a8f84(int,int);void native_fn_020a91a0(const char*,char*,int,int);
#define strncpy native_fn_0201d780
#define strlen native_fn_0201d69c
#define strstr native_fn_0201d984
#define strncmp native_fn_0201d914
#define atoi native_fn_0201f274
#define gpiValueForKey native_fn_020b2ae0
#define gpiCallErrorCallback native_fn_020acbcc
#define gpiSetError native_fn_020b2c6c
#define GSISocketSelect native_fn_020a8ca8
#define Util_RandSeed native_fn_020a8f68
#define Util_RandInt native_fn_020a8f84
#define B64Encode native_fn_020a91a0
extern const char native_data_020e1584[];
extern const char native_data_020e158c[];
extern const char native_data_020e1594[];
extern const char native_data_020e15a0[];
extern const char native_data_020e15a8[];
extern const char native_data_020e15e0[];
