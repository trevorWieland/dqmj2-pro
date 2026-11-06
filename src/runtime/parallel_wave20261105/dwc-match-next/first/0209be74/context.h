typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef int BOOL;typedef int DWCState;typedef void(*DWCLoginCallback)(int,int,void*);typedef void(*DWCUpdateServersCallback)(int,BOOL,void*);typedef void(*DWCMatchedCallback)(int,BOOL,void*);typedef void(*DWCMatchedSCCallback)(int,BOOL,BOOL,BOOL,int,void*);typedef void(*DWCConnectionClosedCallback)(int,BOOL,BOOL,u8,int,void*);
typedef struct{void*connected,*received,*closed,*ping;}GT2ConnectionCallbacks;
typedef struct{u8 opaque0[72];char authToken[256],partnerChallenge[256];}DWCLoginTokensPrefix;
typedef struct{u8 opaque0[13];u8 gt2NumConnection;u8 opaqueE[0x2f0-14];u32 validAidBitmap;}DWCMatchPrefix;
typedef struct{void*gt2Socket;GT2ConnectionCallbacks gt2Callbacks;int gt2SendBufSize,gt2RecvBufSize;void*gpObj,*userdata;DWCState state,lastState;u8 aid,ownCloseFlag;u16 playerName[26];int profileID;const char*gameName,*secretKey;DWCLoginCallback loginCallback;void*loginParam;DWCUpdateServersCallback updateServersCallback;void*updateServersParam;DWCMatchedCallback matchedCallback;void*matchedParam;DWCMatchedSCCallback matchedSCCallback;void*matchedSCParam;DWCConnectionClosedCallback closedCallback;void*closedParam;DWCLoginTokensPrefix logcnt;u8 opaqueFriendSuffix[0x98];DWCMatchPrefix matchcnt;}DWCCorePrefix;
extern DWCCorePrefix*native_data_021d19e0;
#define stpDwcCnt native_data_021d19e0
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define SDK_ASSERT(x) ((void)0)
#define DWC_Printf(...) ((void)0)
#define DWC_MAX_PLAYER_NAME 26
#define DWC_STATE_INIT 0
#define DWC_STATE_AVAILABLE_CHECK 1
#define DWC_STATE_ONLINE 3
#define DWC_STATE_UPDATE_SERVERS 4
#define DWC_STATE_MATCHING 5
#define DWC_STATE_CONNECTED 6
#define DWC_CONNECTINET_STATE_CONNECTED 4
#define DWC_ERROR_AUTH_ANY 2
#define DWC_ECODE_SEQ_LOGIN (-60000)
#define DWC_ECODE_TYPE_NETWORK (-10)
BOOL native_fn_0209a9e4(void);u32 native_fn_0209b438(const u16*);void native_fn_02008be0(u16,void*,u32),native_fn_02008bf8(const void*,void*,u32);int native_fn_0209ad08(void);void native_fn_0209c610(int,int),native_fn_0209be60(DWCState),native_fn_020a932c(const char*);
#define DWCi_IsError native_fn_0209a9e4
#define DWCi_WStrLen native_fn_0209b438
#define MI_CpuClear16(d,n) native_fn_02008be0(0,d,n)
#define MI_CpuCopy16(s,d,n) native_fn_02008bf8(s,d,n)
#define DWC_GetInetStatus native_fn_0209ad08
#define DWCi_StopLogin native_fn_0209c610
#define DWCi_SetState native_fn_0209be60
#define GSIStartAvailableCheck native_fn_020a932c

typedef void(*DWCFriendStatusCallback)(int,u8,const char*,void*);typedef void(*DWCDeleteFriendListCallback)(int,int,void*);
typedef int DWCError;typedef int(*DWCEvalPlayerCallback)(int,void*);typedef void*GT2Connection;
#define DWC_MAX_MATCH_IDX_LIST 64
#define DWC_MAX_CONNECTIONS 32
#define DWC_MATCH_ACCEPT_NO_FRIEND
#define DWC_STATUS_ONLINE 1
#define DWC_ERROR_NONE 0
extern const char native_data_020e016c[];
void native_fn_0209c035(int,BOOL,void*),native_fn_0209c05d(int,BOOL,BOOL,BOOL,int,void*);void native_fn_0209cfe4(const char*,const char*,DWCUpdateServersCallback,void*,DWCFriendStatusCallback,void*,DWCDeleteFriendListCallback,void*);void native_fn_0209bd94(void);int native_fn_0209d120(void);u32 native_fn_0209b368(u32);BOOL native_fn_0209e258(const u8*,int,u8,BOOL,DWCMatchedSCCallback,void*,DWCEvalPlayerCallback,void*);int native_fn_0209d1c8(int,const char*,const char*);void native_fn_0209dd14(void),native_fn_020b4540(void*);void*native_fn_0209bd20(u8);void native_fn_020b4528(void*);BOOL native_fn_0209be20(u8);int native_fn_0209f680(u8**),native_fn_0209f4bc(int,int);
#define DWCi_UpdateServersAsync native_fn_0209cfe4
#define DWCi_UpdateServersCallback native_fn_0209c035
#define DWCi_ClearGT2ConnectionList native_fn_0209bd94
#define DWCi_GetFriendListLen native_fn_0209d120
#define DWCi_GetMathRand32 native_fn_0209b368
#define DWCi_ConnectToFriendsAsync native_fn_0209e258
#define DWCi_MatchedCallback native_fn_0209c05d
#define DWCi_SetGPStatus native_fn_0209d1c8
#define DWCi_NNFreeNegotiateList native_fn_0209dd14
#define gt2CloseAllConnectionsHard native_fn_020b4540
#define DWCi_GetGT2Connection native_fn_0209bd20
#define gt2CloseConnectionHard native_fn_020b4528
#define DWCi_IsValidAID native_fn_0209be20
#define DWCi_GetAllAIDList native_fn_0209f680
#define DWCi_DeleteHostByIndex native_fn_0209f4bc


