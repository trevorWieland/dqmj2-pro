#include "string.h"
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
typedef struct GPIProfile{int profileId,userId;GPIBuddyStatus*buddyStatus;GPIBuddyStatusInfo*buddyStatusInfo;void*cache;char*authSig;int requestCount;char*peerSig;}GPIProfile;
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

#define assert(x)
void*native_fn_020a8a3c(void*,const void*);void native_fn_020a89a4(void*,const void*);GPIBool native_fn_020b0a50(GPConnection*,GPProfile,GPIProfile**);
#define TableLookup native_fn_020a8a3c
#define TableEnter native_fn_020a89a4
#define gpiGetProfile native_fn_020b0a50
