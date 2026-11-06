#include "string.h"
typedef struct{void*profileTable;int num,numBuddies,numBlocked;}GPIProfileList;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPProfile,GPEnum,GPIBool;
typedef struct{char*buffer;int size,len,pos;}GPIBuffer;
typedef struct{void(*callback)(GPConnection*,void*,void*);void*param;}GPICallback;
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;unsigned char opaqueSuffix[48];int productID,namespaceID;unsigned char opaque610[28];GPEnum quietModeFlags;}GPIConnection;

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

typedef unsigned int size_t;
#define GP_PASSWORDENC_LEN ((((GP_PASSWORD_LEN+2)*4)/3)+1)
#define GP_CDKEYENC_LEN ((((GP_CDKEY_LEN+2)*4)/3)+1)
#define GP_XOR_SEED 0x79707367
void native_fn_020b2c98(const char*,char*);GPResult native_fn_020ac6f4(GPConnection*,GPIBuffer*,const char*);GPResult native_fn_020ac710(GPConnection*,GPIBuffer*,int);u32 native_fn_0201d69c(const char*);void native_fn_020a8f68(u32);int native_fn_020a8f84(int,int);void native_fn_020a91a0(const char*,char*,int,int);extern char native_data_021d23f0[];
#define gpiEncodeString native_fn_020b2c98
#define gpiAppendStringToBuffer native_fn_020ac6f4
#define gpiAppendIntToBuffer native_fn_020ac710
#define strlen native_fn_0201d69c
#define Util_RandSeed native_fn_020a8f68
#define Util_RandInt native_fn_020a8f84
#define B64Encode native_fn_020a91a0
#define __GSIACGamename native_data_021d23f0

extern const char native_data_020e0b38[];
extern const char native_data_020e0b44[];
extern const char native_data_020e0b4c[];
extern const char native_data_020e0b54[];
extern const char native_data_020e0ae8[];
extern const char native_data_020e0af4[];
extern const char native_data_020e0b00[];
extern const char native_data_020e0a88[];
extern const char native_data_020e0b64[];
extern const char native_data_020e0abc[];
extern const char native_data_020e0b28[];
extern const char native_data_020e0b30[];

#define GP_PARTNERID_GAMESPY 0
#define GP_FIREWALL 1
#define GPI_SDKREV 3
void native_fn_020aced4(char*,int);void native_fn_020a8b1c(unsigned char*,unsigned int,char*);int native_fn_0200616c(char*,const char*,...);GPIBool native_fn_020b0b90(GPConnection*,char*,char*,GPIProfile**);
#define randomString native_fn_020aced4
#define MD5Digest native_fn_020a8b1c
#define sprintf native_fn_0200616c
#define gpiFindProfileByUser native_fn_020b0b90

extern const char native_data_020e0a0c[];
extern const char native_data_020e0a10[];
extern const char native_data_020e0a14[];
extern const char native_data_020e0a1c[];
extern const char native_data_020e0a24[];
extern const char native_data_020e0a34[];
extern const char native_data_020e0a68[];
extern const char native_data_020e0a70[];
extern const char native_data_020e0a7c[];
extern const char native_data_020e0a88[];
extern const char native_data_020e0a98[];
extern const char native_data_020e0aa0[];
extern const char native_data_020e0aa4[];
extern const char native_data_020e0ab0[];
extern const char native_data_020e0abc[];
extern const char native_data_020e0ac8[];
extern const char native_data_020e0ad4[];
extern const char native_data_020e0ae0[];
extern const char native_data_020e0ae8[];
extern const char native_data_020e0af4[];
extern const char native_data_020e0b00[];
extern const char native_data_020e0b10[];
extern const char native_data_020e0b20[];
extern const char native_data_020e0b28[];
extern const char native_data_020e0b30[];

