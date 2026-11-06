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

typedef struct GPIOperation_s{int type;void*data;GPIBool blocking;GPICallback callback;int state,id;GPResult result;struct GPIOperation_s*pnext;}GPIOperation;
#define GPI_PROFILE_SEARCH 3

typedef void(*GPCallback)(GPConnection*,void*,void*);
#define GPI_START 0
#define GPI_CONNECT 0
#define GPI_NEW_PROFILE 1
#define GPI_GET_INFO 2
#define GPI_REGISTER_UNIQUENICK 4
#define GPI_DELETE_PROFILE 5
#define GPI_REGISTER_CDKEY 6
#define GP_MEMORY_ERROR 1
#define assert(x)
#define gsDebugFormat(...) ((void)0)
void*native_fn_020a927c(u32);void native_fn_020b2c88(GPConnection*,const char*);extern const char native_data_020e0f9c[];
#define gsimalloc native_fn_020a927c
#define Error(c,r,s) {native_fn_020b2c88(c,s);return r;}
GPResult native_fn_020ad830(GPConnection*,GPIOperation*,const char*);GPResult native_fn_020b0910(GPConnection*,GPIOperation*,const char*);GPResult native_fn_020b0a80(GPConnection*,GPIOperation*,const char*);GPResult native_fn_020ae2e4(GPConnection*,GPIOperation*,const char*);GPResult native_fn_020b2908(GPConnection*,GPIOperation*,const char*);GPResult native_fn_020b29a0(GPConnection*,GPIOperation*,const char*);
#define gpiProcessConnect native_fn_020ad830
#define gpiProcessNewProfile native_fn_020b0910
#define gpiProcessDeleteProfle native_fn_020b0a80
#define gpiProcessGetInfo native_fn_020ae2e4
#define gpiProcessRegisterUniqueNick native_fn_020b2908
#define gpiProcessRegisterCdKey native_fn_020b29a0

#define GP_UNIQUENICK_LEN 21
#define GP_PASSWORD_LEN 31
#define GP_AUTHTOKEN_LEN 256
#define GP_PARTNERCHALLENGE_LEN 256
#define GP_CDKEY_LEN 65
#define GP_PARAMETER_ERROR 2
#define GPI_NOT_CONNECTED 0
#define GPI_DISCONNECTED 4
#define GS_WIRELESS_DEVICE 1
#define CHECK_RESULT(f) {GPResult checked=(f);if(checked!=GP_NO_ERROR)return checked;}
typedef struct{char serverChallenge[128],userChallenge[33],passwordHash[33],authtoken[256],partnerchallenge[256],cdkey[65];GPIBool newuser;}GPIConnectData;
GPResult native_fn_020aa9b4(GPConnection*);void native_fn_020b2a38(char*,const char*,int);char*native_fn_020a8ec4(char*);void*native_fn_0201b208(void*,int,u32);GPResult native_fn_020afa1c(GPConnection*,int,void*,GPIOperation**,GPEnum,GPCallback,void*);GPResult native_fn_020acf00(GPConnection*,GPIOperation*);GPResult native_fn_020af7f8(GPConnection*,const GPIOperation*);void native_fn_020ade3c(GPConnection*,GPIBool);GPResult native_fn_020aae0c(GPConnection*,int);extern const char native_data_020e09e8[],native_data_020e09fc[];
#define gpiReset native_fn_020aa9b4
#define strzcpy native_fn_020b2a38
#define _strlwr native_fn_020a8ec4
#define memset native_fn_0201b208
#define gpiAddOperation native_fn_020afa1c
#define gpiStartConnect native_fn_020acf00
#define gpiFailedOpCallback native_fn_020af7f8
#define gpiDisconnect native_fn_020ade3c
#define gpiProcess native_fn_020aae0c

typedef void*DArray;typedef struct{char*keyName,*keyValue;}GPIKey;typedef unsigned int size_t;
#define GS_ASSERT(x)
#define NOT_FOUND (-1)
char*native_fn_020a8ea0(const char*);void native_fn_020a929c(void*);void native_fn_020a8614(DArray);void native_fn_020a86b8(DArray,const void*,int(*)(const void*,const void*));int native_fn_020a8764(DArray,const void*,int(*)(const void*,const void*),int,int);void*native_fn_020a8644(DArray,int);int native_fn_020a8640(DArray);int native_fn_020af4b0(const void*,const void*);u32 native_fn_0201d69c(const char*);int native_fn_0200616c(char*,const char*,...);char*native_fn_0201d7d0(char*,const char*);void native_fn_020a91a0(const char*,char*,int,int);
#define goastrdup native_fn_020a8ea0
#define gsifree native_fn_020a929c
#define freeclear(p) do{gsifree(p);(p)=NULL;}while(0)
#define ArrayFree native_fn_020a8614
#define ArrayInsertSorted native_fn_020a86b8
#define ArraySearch native_fn_020a8764
#define ArrayNth native_fn_020a8644
#define ArrayLength native_fn_020a8640
#define gpiStatusInfoKeyCompFunc native_fn_020af4b0
#define strlen native_fn_0201d69c
#define sprintf native_fn_0200616c
#define strcat native_fn_0201d7d0
#define B64Encode native_fn_020a91a0

extern const char native_data_020e0f54[];
extern const char native_data_020e0f64[];
extern const char native_data_020e0f78[];
extern const char native_data_020e0f8c[];
extern const char native_data_020e0f98[];
