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
typedef struct{char errorString[256];GPIBool infoCaching,infoCachingBuddyAndBlockOnly,simulation,firewall;char nick[31],uniquenick[21],email[51],password[31];int sessKey,userid,profileid,partnerID;GPICallback callbacks[9];int cmSocket,connectState;GPIBuffer socketBuffer;char*inputBuffer;int inputBufferSize;GPIBuffer outputBuffer;char mHeader[16];u16 peerPort;int nextOperationID,numSearches;GPEnum lastStatusState;u32 hostIp,hostPrivateIp;u16 queryPort,hostPort;u32 sessionFlags;char richStatus[256],gameType[33],gameVariant[33],gameMapName[33];void*extendedInfoKeys;char lastStatusString[256],lastLocationString[256];int errorCode;GPIBool fatalError;void*diskCache,*operationList;GPIProfileList profileList;GPIPeer*peerList;u32 callbackSlots[2];GPIBuffer updateproBuffer,updateuiBuffer;}GPIConnection;

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

typedef int GSUdpErrorCode,GSUdpPeerState;
#define GS_UDP_PEER_CONNECTING 0
#define GS_UDP_PEER_CONNECTED 1
#define GS_UDP_ADDRESS_ALREADY_IN_USE 5
#define GPI_PEER_CONNECTING 103
#define GP_NETWORK 5
#define Error(c,r,s) {native_fn_020b2c88(c,s);return r;}
#define CallbackError(c,r,e,s) do{native_fn_020b2c6c(c,e,s);native_fn_020acbcc(c,r,0);return r;}while(0)
void native_fn_020b2c88(GPConnection*,const char*),native_fn_020b2c6c(GPConnection*,int,const char*),native_fn_020acbcc(GPConnection*,GPResult,GPEnum);GSUdpErrorCode native_fn_020a9aa8(u32,u16,GSUdpPeerState*),native_fn_020a9b08(u32,u16,char*,int);
#define gsUdpEngineGetPeerState native_fn_020a9aa8
#define gsUdpEngineStartTalkingToPeer native_fn_020a9b08
extern const char native_data_020e1060[];
extern const char native_data_020e0fac[];

void*native_fn_020a927c(u32);unsigned long native_fn_0201d69c(const char*);
#define gsimalloc native_fn_020a927c

#define CHECK_RESULT(f) {GPResult checked=(f);if(checked!=GP_NO_ERROR)return checked;}

#define GPI_PEER_GETTING_SIG 101
#define GPI_PEER_GOT_SIG 102
#define GPI_PEER_WAITING 104
#define GPI_PEER_CONNECTED 105
#define GPI_PEER_DISCONNECTED 106
#define GS_UDP_PEER_CLOSED 3
GPResult native_fn_020b049c(GPConnection*,GPIPeer*),native_fn_020b0464(GPConnection*,GPIPeer*),native_fn_020ac9e8(GPConnection*,u32,u16,GPIBuffer*,GPIBool*,GPIBool);GPIBool native_fn_020b0ca8(GPIProfile*);void native_fn_020b0b48(GPConnection*,GPIProfile*);char*native_fn_0201d984(const char*,const char*);int native_fn_0201d914(const char*,const char*,u32),native_fn_0201f274(const char*),native_fn_0201d800(const char*,const char*),native_fn_0200616c(char*,const char*,...);GPIBool native_fn_020b2ae0(const char*,const char*,char*,int);void native_fn_020a8b1c(unsigned char*,unsigned int,char*);
#define gpiPeerStartConnect native_fn_020b049c
#define gpiPeerGetSig native_fn_020b0464
#define gpiSendBufferToPeer native_fn_020ac9e8
#define gpiCanFreeProfile native_fn_020b0ca8
#define gpiRemoveProfile native_fn_020b0b48
#define atoi native_fn_0201f274
#define sprintf native_fn_0200616c
#define gpiValueForKey native_fn_020b2ae0
#define MD5Digest native_fn_020a8b1c
#define ArrayLength native_fn_020a8640
#define ArrayNth native_fn_020a8644
#define ArrayDeleteAt native_fn_020a8720
int native_fn_020a8640(void*);void*native_fn_020a8644(void*,int);void native_fn_020a8720(void*,int);
extern const char native_data_020e0ff8[];
extern const char native_data_020e0fd8[];
extern const char native_data_020e0ff0[];
extern const char native_data_020e0fe8[];
extern const char native_data_020e101c[];
extern const char native_data_020e0fd0[];
extern const char native_data_020e1024[];
extern const char native_data_020e0fac[];
extern const char native_data_020e0fe0[];
extern const char native_data_020e0fc8[];

#define gsDebugFormat(...) ((void)0)

#define GPI_BM_MESSAGE 1
#define GPI_BM_REQUEST 2
#define GPI_BM_REPLY 3
#define GPI_BM_AUTH 4
#define GPI_BM_UTM 5
#define GPI_BM_REVOKE 6
#define GPI_BM_STATUS 100
#define GPI_BM_INVITE 101
#define GPI_BM_PING 102
#define GPI_BM_PONG 103
#define GPI_BM_KEYS_REQUEST 104
#define GPI_BM_KEYS_REPLY 105
#define GPI_BM_FILE_SEND_REQUEST 200
#define GPI_BM_FILE_SEND_REPLY 201
#define GPI_BM_FILE_BEGIN 202
#define GPI_BM_FILE_END 203
#define GPI_BM_FILE_DATA 204
#define GPI_BM_FILE_SKIP 205
#define GPI_BM_FILE_TRANSFER_THROTTLE 206
#define GPI_BM_FILE_TRANSFER_CANCEL 207
#define GPI_BM_FILE_TRANSFER_KEEPALIVE 208
#define NOFILE
#define GPI_RECV_BUDDY_MESSAGE 3
#define GPI_RECV_BUDDY_UTM 4
#define GPI_ADD_MESSAGE 2
#define GP_MEMORY_ERROR 1
typedef struct{GPProfile profile;u32 date;char*message;}GPRecvBuddyMessageArg,GPRecvBuddyUTMArg;
GPResult native_fn_020aff44(GPConnection*,GPIPeer*),native_fn_020acae0(GPConnection*,GPIBuffer*,char**,int*,int*),native_fn_020acc28(GPConnection*,GPICallback,void*,const GPIOperation*,int),native_fn_020abfe4(GPConnection*,int,int,const char*,int,GPIPeerOp*),native_fn_020ac0d8(GPConnection*,GPIPeer*),native_fn_020ac130(GPConnection*,GPIPeer*,char*),native_fn_020acb98(GPConnection*,GPIBuffer*);void native_fn_020b28c0(GPConnection*,GPIPeer*,int,const char*,const char*,int);char*native_fn_020a8ea0(const char*);
#define gpiPeerSendMessages native_fn_020aff44
#define gpiReadMessageFromBuffer native_fn_020acae0
#define gpiAddCallback native_fn_020acc28
#define goastrdup native_fn_020a8ea0
#define gpiSendBuddyMessage native_fn_020abfe4
#define gpiBuddyHandleKeyRequest native_fn_020ac0d8
#define gpiBuddyHandleKeyReply native_fn_020ac130
#define gpiHandleTransferMessage native_fn_020b28c0
#define gpiClipBufferToPosition native_fn_020acb98
extern const char native_data_020e104c[];
extern const char native_data_020e105c[];
