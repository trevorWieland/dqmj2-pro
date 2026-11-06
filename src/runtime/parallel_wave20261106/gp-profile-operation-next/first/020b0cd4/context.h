#include "string.h"
typedef struct GPIPeer_s GPIPeer;
typedef struct{void*profileTable;int num,numBuddies;}GPIProfileList;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef void*GPConnection;typedef int GPResult,GPProfile,GPEnum,GPIBool;
typedef struct{char*buffer;int size,len,pos;}GPIBuffer;
typedef long time_t;typedef unsigned int gsi_time;typedef int GPIPeerOpState;typedef void*DArray;typedef void(*GPCallback)(GPConnection*,void*,void*);
typedef struct GPIMessage
{
	GPIBuffer buffer;
	int type;
	int start;
} GPIMessage;

typedef struct _GPIPeerOp
{
	GPIPeerOpState state;
	void *userData;
	GPCallback callback;
	struct _GPIPeerOp * next;
	int type;
	gsi_time timeout;
} GPIPeerOp;

typedef struct _GPIPeerOpQueue
{
	GPIPeerOp * opList;
	GPIPeerOp * first;
	GPIPeerOp * last;
} GPIPeerOpQueue;



typedef struct GPIPeer_s
{
	int state;
	GPIBool initiated;
	
	unsigned int ip;
	unsigned short port;
	GPProfile profile;
	time_t timeout;
	int nackCount;
	GPIBuffer inputBuffer;
	GPIBuffer outputBuffer;
	DArray messages;
	GPIPeerOpQueue peerOpQueue;
	struct GPIPeer_s * pnext;
} GPIPeer;
typedef struct{void(*callback)(GPConnection*,void*,void*);void*param;}GPICallback;
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;GPIPeer*peerList;u32 callbackSlots[2];GPIBuffer updateproBuffer,updateuiBuffer;u8 unknownBeforeKeepalive[48];u32 kaTransmit;}GPIConnection;

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

typedef int SOCKET;
#define INVALID_SOCKET (-1)
#define GPI_CONNECTED 3
#define GPI_DISCONNECTED 4
#define GPI_NOT_CONNECTED 0
GPResult native_fn_020ac6f4(GPConnection*,GPIBuffer*,const char*);GPResult native_fn_020ac710(GPConnection*,GPIBuffer*,int);GPResult native_fn_020ac954(GPConnection*,SOCKET,GPIBuffer*,GPIBool*,GPIBool,const char*);int native_fn_020a8b7c(SOCKET,int);int native_fn_020a8b6c(SOCKET);GPIBool native_fn_020a99c0(void);void native_fn_020a9e0c(const char*);GPIBool native_fn_020a9e70(void),native_fn_020a9e94(void);void native_fn_020a9d38(void),native_fn_020a929c(void*);void native_fn_020afad8(GPConnection*,GPIOperation*),native_fn_020b029c(GPConnection*,GPIPeer*);GPIBool native_fn_020add5c(GPConnection*,GPIProfile*,void*);
#define gpiAppendStringToBuffer native_fn_020ac6f4
#define gpiAppendIntToBuffer native_fn_020ac710
#define gpiSendFromBuffer native_fn_020ac954
#define shutdown native_fn_020a8b7c
#define closesocket native_fn_020a8b6c
#define gsUdpEngineIsInitialized native_fn_020a99c0
#define gsUdpEngineRemoveMsgHandler native_fn_020a9e0c
#define gsUdpEngineNoMoreMsgHandlers native_fn_020a9e70
#define gsUdpEngineNoApp native_fn_020a9e94
#define gsUdpEngineShutdown native_fn_020a9d38
#define gsifree native_fn_020a929c
#define freeclear(p) do{gsifree(p);(p)=NULL;}while(0)
#define gpiRemoveOperation native_fn_020afad8
#define gpiDestroyPeer native_fn_020b029c
#define gpiDisconnectCleanupProfile native_fn_020add5c
extern const char native_data_020e0c68[];
extern const char native_data_020e0c54[];
extern const char native_data_020e0b30[];

#define GS_ASSERT(x)
#define GPI_PEER_NOT_CONNECTED 100
#define GPI_PEER_TIMEOUT 10000
#define GP_NETWORK_ERROR 3
long native_fn_020a8e7c(long*);void*native_fn_020a85dc(int,int,void(*)(void*));void native_fn_020b03f4(void*),native_fn_020a865c(void*,const void*);GPResult native_fn_020ac684(GPConnection*,GPIBuffer*,const char*,int),native_fn_020ac63c(GPConnection*,GPIBuffer*,int);
#define time native_fn_020a8e7c
#define ArrayNew native_fn_020a85dc
#define gpiFreeMessage native_fn_020b03f4
#define ArrayAppend native_fn_020a865c
#define gpiAppendStringToBufferLen native_fn_020ac684
#define gpiAppendCharToBuffer native_fn_020ac63c
extern const char native_data_020e1098[];
extern const char native_data_020e109c[];
extern const char native_data_020e10a4[];

void*native_fn_020a927c(u32);unsigned long native_fn_0201d69c(const char*);
#define gsimalloc native_fn_020a927c
#define strlen native_fn_0201d69c

#define CHECK_RESULT(f) {GPResult checked=(f);if(checked!=GP_NO_ERROR)return checked;}

#define GP_ERROR 2
#define RAND_MAX 0x7fff
#define INVALID_SOCKET (-1)
#define GPI_NOT_CONNECTED 0
#define gpiStatusInfoKeysDestroy native_fn_020af494
#define gpiStatusInfoKeysInit native_fn_020af460
#define gpiDestroy native_fn_020aa978
#define gpiResetProfile native_fn_020aa9a4
void native_fn_020af494(GPConnection*),native_fn_020aa978(GPConnection*);
GPResult native_fn_020af460(GPConnection*);
GPIBool native_fn_020aa9a4(GPConnection*,GPIProfile*,void*);
extern const char native_data_020e0890[];
#define RANDSTRING native_data_020e0890
#define RANDOMCHAR() (RANDSTRING[rand()%62])

GPResult
native_main_020aa9b4(
  GPConnection * connection
);

typedef int GSUdpErrorCode;
typedef void(*gsUdpErrorCallback)(GSUdpErrorCode,void*);
typedef void(*gsUdpConnConnectedCallback)(u32,u16,GSUdpErrorCode,int,void*);
typedef void(*gsUdpConnClosedCallback)(u32,u16,int,void*);
typedef void(*gsUdpConnPingCallback)(u32,u16,u32,void*);
typedef void(*gsUdpConnReceivedDataCallback)(u32,u16,u8*,u32,int,void*);
typedef int(*gsUdpUnknownMsgCallback)(u32,u16,u8*,u32,void*);
typedef void(*gsUdpAppConnectAttemptCallback)(u32,u16,int,u8*,u32,void*);
struct in_addr{u32 s_addr;};
struct sockaddr_in{u8 sin_len,sin_family;u16 sin_port;struct in_addr sin_addr;};
struct sockaddr{u8 len,family;u8 address[6];};
struct hostent{char*h_name;char**h_aliases;short h_addrtype,h_length;char**h_addr_list;};
#define gsDebugFormat(...)
#define GS_UDP_MSG_HEADER_LEN 16
#define GPI_PEER_PORT 6500
#define GPI_CONNECTION_MANAGER_PORT 29900
#define GS_UDP_NO_ERROR 0
#define GP_UDP_LAYER 8
#define GP_NETWORK 5
#define GPI_CONNECTING 1
#define AF_INET 2
#define SOCK_STREAM 1
#define INADDR_NONE 0xffffffffU
#define WSAEWOULDBLOCK (-6)
#define WSAEINPROGRESS (-26)
#define WSAETIMEDOUT (-76)
#define gsiSocketIsError(r) ((r)==-1)
#define GPI_UDP_HEADER native_data_020e08d0
#define GPConnectionManagerHostname native_data_020e0850
#define htons(x) ((u16)((((u16)(x)>>8)&0x00ff)|(((u16)(x)<<8)&0xff00)))
GSUdpErrorCode native_fn_020a99cc(u16,int,int,gsUdpConnConnectedCallback,gsUdpConnClosedCallback,gsUdpConnPingCallback,gsUdpConnReceivedDataCallback,gsUdpErrorCallback,gsUdpUnknownMsgCallback,gsUdpAppConnectAttemptCallback,void*);
u16 native_fn_020a9d64(void);
GSUdpErrorCode native_fn_020a9d78(const void*,const void*,gsUdpErrorCallback,gsUdpConnConnectedCallback,gsUdpConnClosedCallback,gsUdpConnPingCallback,gsUdpConnReceivedDataCallback,void*);
void native_fn_020b0770(u32,u16,GSUdpErrorCode,int,void*),native_fn_020b06b8(u32,u16,int,void*),native_fn_020b0790(u32,u16,u32,void*),native_fn_020b06d0(u32,u16,u8*,u32,int,void*);
int native_fn_020a8b5c(int,int,int),native_fn_020a8d54(int,int),native_fn_020a8bc4(int,const struct sockaddr*,int),native_fn_020a8c9c(int);
u32 native_fn_020a8c84(const char*);
struct hostent*native_fn_0209046c(const char*);
void native_fn_020b2c6c(GPConnection*,int,const char*),native_fn_020acbcc(GPConnection*,GPResult,GPIBool);
#define gsUdpEngineIsInitialized native_fn_020a99c0
#define gsUdpEngineInitialize native_fn_020a99cc
#define gsUdpEngineGetLocalPort native_fn_020a9d64
#define gsUdpEngineAddMsgHandler native_fn_020a9d78
#define gpiPeerAcceptedCallback native_fn_020b0770
#define gpiPeerLeftCallback native_fn_020b06b8
#define gpiPeerPingReplyCallback native_fn_020b0790
#define gpiPeerMessageCallback native_fn_020b06d0
#define socket native_fn_020a8b5c
#define connect native_fn_020a8bc4
#define SetSockBlocking native_fn_020a8d54
#define inet_addr native_fn_020a8c84
#define gethostbyname native_fn_0209046c
#define GOAGetLastError native_fn_020a8c9c
#define CallbackFatalError(connection,result,code,string) {native_fn_020b2c6c(connection,code,string);native_fn_020acbcc(connection,result,1);return(result);}

extern const char native_data_020e0850[];
extern const char native_data_020e08d0[];
extern const char native_data_020e08dc[];
extern const char native_data_020e0904[];
extern const char native_data_020e0930[];
extern const char native_data_020e0958[];
extern const char native_data_020e098c[];
extern const char native_data_020e09c0[];

GPResult
native_main_020acf00(
  GPConnection * connection,
  GPIOperation * operation
);

typedef struct{int type;SOCKET sock;GPIBuffer inputBuffer,outputBuffer;char nick[31],uniquenick[21],email[51],firstname[31],lastname[31],password[31],cdkey[65];int partnerID,icquin,skip,productID;GPIBool processing,remove;gsi_time searchStartTime;int*revBuddyProfileIds;int numOfRevBuddyProfiles;}GPISearchData;
#define IPPROTO_TCP 0
#define GPI_SEARCH_MANAGER_PORT 29901
u32 native_fn_020a8ef8(void);
#define current_time native_fn_020a8ef8
#define Error(connection,result,string) {native_fn_020b2c88(connection,string);return(result);}
void native_fn_020b2c88(GPConnection*,const char*);

extern const char native_data_020e1130[];
extern const char native_data_020e1170[];
extern const char native_data_020e1180[];
extern const char native_data_020e11a8[];
extern const char native_data_020e11dc[];
extern const char native_data_020e120c[];

GPResult
native_main_020b0cd4(
  GPConnection * connection,
  GPIOperation * operation
);

#define GP_MEMORY_ERROR 1
