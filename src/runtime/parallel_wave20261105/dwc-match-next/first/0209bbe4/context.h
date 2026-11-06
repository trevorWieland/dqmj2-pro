typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef int BOOL;typedef int DWCState;typedef void(*DWCLoginCallback)(int,int,void*);typedef void(*DWCUpdateServersCallback)(int,BOOL,void*);typedef void(*DWCMatchedCallback)(int,BOOL,void*);typedef void(*DWCMatchedSCCallback)(int,BOOL,BOOL,BOOL,int,void*);typedef void(*DWCConnectionClosedCallback)(int,BOOL,BOOL,u8,int,void*);
typedef struct{void*connected,*received,*closed,*ping;}GT2ConnectionCallbacks;
typedef struct{void*gt2Socket;GT2ConnectionCallbacks gt2Callbacks;int gt2SendBufSize,gt2RecvBufSize;void*gpObj,*userdata;DWCState state,lastState;u8 aid,ownCloseFlag;u16 playerName[26];int profileID;const char*gameName,*secretKey;DWCLoginCallback loginCallback;void*loginParam;DWCUpdateServersCallback updateServersCallback;void*updateServersParam;DWCMatchedCallback matchedCallback;void*matchedParam;DWCMatchedSCCallback matchedSCCallback;void*matchedSCParam;DWCConnectionClosedCallback closedCallback;void*closedParam;}DWCCorePrefix;
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
