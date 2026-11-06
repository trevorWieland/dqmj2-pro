typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef int gsi_bool,GT2Bool,GT2Result,GT2ConnectionState,GT2CloseReason,GSUdpErrorCode,GSUdpPeerState,GSUdpCloseReason;typedef u8 GT2Byte;typedef void*GT2Socket;typedef void*GT2Connection;typedef void*DArray;
typedef void(*gsUdpErrorCallback)(GSUdpErrorCode,void*);
typedef void(*gsUdpConnConnectedCallback)(u32,u16,GSUdpErrorCode,gsi_bool,void*);
typedef void(*gsUdpConnClosedCallback)(u32,u16,GSUdpCloseReason,void*);
typedef void(*gsUdpConnPingCallback)(u32,u16,u32,void*);
typedef void(*gsUdpConnReceivedDataCallback)(u32,u16,u8*,u32,gsi_bool,void*);
typedef gsi_bool(*gsUdpUnknownMsgCallback)(u32,u16,u8*,u32,void*);
typedef void(*gsUdpAppConnectAttemptCallback)(u32,u16,int,u8*,u32,void*);
typedef struct{void(*connected)(GT2Connection,GT2Result,GT2Byte*,int);void(*received)(GT2Connection,GT2Byte*,int,GT2Bool);void(*closed)(GT2Connection,GT2CloseReason);void(*ping)(GT2Connection,int);}GT2ConnectionCallbacks;
typedef struct{u32 mAddr;u16 mPort;GT2Connection mConnection;}GSUdpRemotePeer;
typedef struct{u8 mInitialMsg[16],mHeader[16];DArray mPendingConnections;gsUdpConnClosedCallback mClosed;gsUdpConnReceivedDataCallback mReceived;gsUdpConnConnectedCallback mConnected;gsUdpConnPingCallback mPingReply;gsUdpErrorCallback mNetworkError;void*mUserData;}GSUdpMsgHandler;
typedef struct{GT2Socket mSocket;DArray mRemotePeers,mMsgHandlers;gsi_bool mInitialized;gsUdpConnConnectedCallback mAppConnected;gsUdpConnClosedCallback mAppClosed;gsUdpConnPingCallback mAppPingReply;gsUdpConnReceivedDataCallback mAppRecvData;gsUdpAppConnectAttemptCallback mAppConnAttempt;gsUdpErrorCallback mAppNetworkError;gsUdpUnknownMsgCallback mAppUnknownMessage;void*mAppUserData;int mAppPendingConnections;u32 mLocalAddr;u16 mLocalPort;}GSUdpEngineObject;
#define NULL ((void*)0)
#define GS_UDP_MSG_HEADER_LEN 16
#define GS_IP_ADDR_AND_PORT 22
#define GS_UDP_DEFAULT_IN_BUFFSIZE 1500
#define GS_UDP_DEFAULT_OUT_BUFFSIZE 1460
#define NOT_FOUND -1
#define gsi_true 1
#define gsi_false 0
#define GT2True 1
#define GT2False 0
#define GT2Success 0
#define GT2Connected 1
#define GT2Connecting 0
#define GS_ASSERT(x)
#define GSI_UNUSED(x) ((void)(x))
#define gsDebugFormat(...)
enum{GS_UDP_NO_ERROR,GS_UDP_NO_MEMORY,GS_UDP_REJECTED,GS_UDP_NETWORK_ERROR,GS_UDP_ADDRESS_ERROR,GS_UDP_ADDRESS_ALREADY_IN_USE,GS_UDP_TIMED_OUT,GS_UDP_REMOTE_ERROR,GS_UDP_SEND_FAILED,GS_UDP_INVALID_MESSAGE,GS_UDP_PARAMETER_ERROR,GS_UDP_NOT_INITIALIZED,GS_UDP_MSG_TOO_BIG};
#define GS_UDP_PEER_CLOSED 3
GSUdpEngineObject*native_fn_020a9508(void);
void native_fn_020a9510(void*);
int native_fn_020a951c(const void*,const void*);int native_fn_020a9528(const void*,const void*);int native_fn_020a9538(const void*,const void*);
void native_fn_020a9564(GT2Socket);
void native_fn_020a95a8(GT2Connection,GT2CloseReason);
void native_fn_020a9664(GT2Connection,GT2Result,GT2Byte*,int);
void native_fn_020a97b4(GT2Connection,int);
void native_fn_020a9828(GT2Connection,GT2Byte*,int,GT2Bool);
GT2Bool native_fn_020a98d4(GT2Socket,u32,u16,GT2Byte*,int);
void native_fn_020a9904(GT2Socket,GT2Connection,u32,u16,int,GT2Byte*,int);
DArray native_fn_020a85dc(int,int,void(*)(void*));void native_fn_020a865c(DArray,const void*);int native_fn_020a8764(DArray,const void*,int(*)(const void*,const void*),int,int);int native_fn_020a8640(DArray);void*native_fn_020a8644(DArray,int);void native_fn_020a86ec(DArray,int);void native_fn_020a8720(DArray,int);
char*native_fn_020b5f38(u32,u16,char*);
GT2Bool native_fn_020b437c(GT2Connection,GT2ConnectionCallbacks*);void native_fn_020b4384(GT2Connection,const GT2Byte*,int);
GT2Result native_fn_020b4330(GT2Socket*,const char*,int,int,void(*)(GT2Socket));
void native_fn_020b45a4(GT2Socket,GT2Bool(*)(GT2Socket,u32,u16,GT2Byte*,int));void native_fn_020b4374(GT2Socket,void(*)(GT2Socket,GT2Connection,u32,u16,int,GT2Byte*,int));u32 native_fn_020b458c(GT2Socket);u16 native_fn_020b4590(GT2Socket);
GT2ConnectionState native_fn_020b4568(GT2Connection);GT2Result native_fn_020b438c(GT2Socket,GT2Connection*,const char*,const GT2Byte*,int,int,GT2ConnectionCallbacks*,GT2Bool);
int native_fn_020b4594(GT2Connection);int native_fn_020b4598(GT2Connection);GT2Result native_fn_020b4480(GT2Connection,const GT2Byte*,int,GT2Bool);
void*native_fn_020a927c(unsigned long);void native_fn_020a929c(void*);void*native_fn_0201b19c(void*,const void*,u32);
static inline void*copy16(void*dst,const void*src,u32 ignored){u8*d=dst;const u8*s=src;u32 left=16;do{*d++=*s++;}while(--left);return dst;}
#define gsUdpEngineGetEngine native_fn_020a9508
#define gsUdpMsgHandlerFree native_fn_020a9510
#define gsUdpMsgHandlerCompare native_fn_020a951c
#define gsUdpMsgHandlerCompare2 native_fn_020a9528
#define gsUdpRemotePeerCompare native_fn_020a9538
#define gsUdpSocketError native_fn_020a9564
#define gsUdpClosedRoutingCB native_fn_020a95a8
#define gsUdpConnectedRoutingCB native_fn_020a9664
#define gsUdpPingRoutingCB native_fn_020a97b4
#define gsUdpReceivedRoutingCB native_fn_020a9828
#define gsUdpUnrecognizedMsgCB native_fn_020a98d4
#define gsUdpConnAttemptCB native_fn_020a9904
#define ArrayNew native_fn_020a85dc
#define ArrayAppend native_fn_020a865c
#define ArraySearch native_fn_020a8764
#define ArrayLength native_fn_020a8640
#define ArrayNth native_fn_020a8644
#define ArrayRemoveAt native_fn_020a86ec
#define ArrayDeleteAt native_fn_020a8720
#define gt2AddressToString native_fn_020b5f38
#define gt2Accept native_fn_020b437c
#define gt2Reject native_fn_020b4384
#define gt2CreateSocket native_fn_020b4330
#define gt2SetUnrecognizedMessageCallback native_fn_020b45a4
#define gt2Listen native_fn_020b4374
#define gt2GetLocalIP native_fn_020b458c
#define gt2GetLocalPort native_fn_020b4590
#define gt2GetConnectionState native_fn_020b4568
#define gt2Connect native_fn_020b438c
#define gt2GetOutgoingBufferSize native_fn_020b4594
#define gt2GetOutgoingBufferFreeSpace native_fn_020b4598
#define gt2Send native_fn_020b4480
#define gsimalloc native_fn_020a927c
#define gsifree native_fn_020a929c
#define memcpy native_fn_0201b19c
