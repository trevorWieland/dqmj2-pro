#define DWCi_StopMatching native_fn_0209f130
#define DWCi_StopFriendProcess native_fn_0209d03c
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef int BOOL;typedef int DWCState;typedef void(*DWCLoginCallback)(int,int,void*);typedef void(*DWCUpdateServersCallback)(int,BOOL,void*);typedef void(*DWCMatchedCallback)(int,BOOL,void*);typedef void(*DWCMatchedSCCallback)(int,BOOL,BOOL,BOOL,int,void*);typedef void(*DWCConnectionClosedCallback)(int,BOOL,BOOL,u8,int,void*);
typedef struct{void*connected,*received,*closed,*ping;}GT2ConnectionCallbacks;
typedef struct{void*gt2Socket;GT2ConnectionCallbacks gt2Callbacks;int gt2SendBufSize,gt2RecvBufSize;void*gpObj,*userdata;DWCState state,lastState;u8 aid,ownCloseFlag;u16 playerName[26];int profileID;const char*gameName,*secretKey;DWCLoginCallback loginCallback;void*loginParam;DWCUpdateServersCallback updateServersCallback;void*updateServersParam;DWCMatchedCallback matchedCallback;void*matchedParam;DWCMatchedSCCallback matchedSCCallback;void*matchedSCParam;DWCConnectionClosedCallback closedCallback;void*closedParam;struct{void*pGpObj;int state;}logcnt;}DWCCorePrefix;
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
BOOL native_fn_0209a9e4(void);u32 native_fn_0209b438(const u16*);void native_fn_02008be0(u16,void*,u32),native_fn_02008bf8(const void*,void*,u32);int native_fn_0209ad08(void);void native_fn_0209c610(int,int),native_fn_0209be60(DWCState),native_fn_020a932c(const char*);
#define DWCi_IsError native_fn_0209a9e4
#define DWCi_WStrLen native_fn_0209b438
#define MI_CpuClear16(d,n) native_fn_02008be0(0,d,n)
#define MI_CpuCopy16(s,d,n) native_fn_02008bf8(s,d,n)
#define DWC_GetInetStatus native_fn_0209ad08
#define DWCi_StopLogin native_fn_0209c610
#define DWCi_SetState native_fn_0209be60
#define GSIStartAvailableCheck native_fn_020a932c

typedef enum {
    DWC_ERROR_NONE = 0,
    DWC_ERROR_DS_MEMORY_ANY,
    DWC_ERROR_AUTH_ANY,
    DWC_ERROR_AUTH_OUT_OF_SERVICE,
    DWC_ERROR_AUTH_STOP_SERVICE,
    DWC_ERROR_AC_ANY,
    DWC_ERROR_NETWORK,
    DWC_ERROR_GHTTP_ANY,
    DWC_ERROR_DISCONNECTED,
    DWC_ERROR_FATAL,
    DWC_ERROR_FRIENDS_SHORTAGE,
    DWC_ERROR_NOT_FRIEND_SERVER,
    DWC_ERROR_MO_SC_CONNECT_BLOCK,
    DWC_ERROR_SERVER_FULL,
    DWC_ERROR_ND_ANY,
    DWC_ERROR_ND_HTTP,
    DWC_ERROR_SVL_ANY,
    DWC_ERROR_SVL_HTTP,
    DWC_ERROR_PROF_ANY,
    DWC_ERROR_PROF_HTTP,
    DWC_ERROR_NUM
} DWCError;
enum {
    DWC_ECODE_SEQ_LOGIN            = (-60000),
    DWC_ECODE_SEQ_FRIEND           = (-70000),
    DWC_ECODE_SEQ_MATCH            = (-80000),
    DWC_ECODE_SEQ_ETC              = (-90000),
    DWC_ECODE_GS_GP                = (-1000),
    DWC_ECODE_GS_PERS              = (-2000),
    DWC_ECODE_GS_STATS             = (-3000),
    DWC_ECODE_GS_QR2               = (-4000),
    DWC_ECODE_GS_SB                = (-5000),
    DWC_ECODE_GS_NN                = (-6000),
    DWC_ECODE_GS_GT2               = (-7000),
    DWC_ECODE_GS_HTTP              = (-8000),
    DWC_ECODE_GS_ETC               = (-9000),
    DWC_ECODE_TYPE_NETWORK         = (-10),
    DWC_ECODE_TYPE_SERVER          = (-20),
    DWC_ECODE_TYPE_DNS             = (-30),
    DWC_ECODE_TYPE_DATA            = (-40),
    DWC_ECODE_TYPE_SOCKET          = (-50),
    DWC_ECODE_TYPE_BIND            = (-60),
    DWC_ECODE_TYPE_TIMEOUT         = (-70),
    DWC_ECODE_TYPE_PEER            = (-80),
    DWC_ECODE_TYPE_CONN_OVER       = (-100),
    DWC_ECODE_TYPE_STATS_AUTH      = (-200),
    DWC_ECODE_TYPE_STATS_LOAD      = (-210),
    DWC_ECODE_TYPE_STATS_SAVE      = (-220),
    DWC_ECODE_TYPE_NOT_FRIEND      = (-400),
    DWC_ECODE_TYPE_OTHER           = (-410),
    DWC_ECODE_TYPE_MUCH_FAILURE    = (-420),
    DWC_ECODE_TYPE_SC_CL_FAIL      = (-430),
    DWC_ECODE_TYPE_CLOSE           = (-600),
    DWC_ECODE_TYPE_TRANS_HEADER    = (-610),
    DWC_ECODE_TYPE_TRANS_BODY      = (-620),
    DWC_ECODE_TYPE_AC_FATAL        = (-700),
    DWC_ECODE_TYPE_OPEN_FILE       = (-800),
    DWC_ECODE_TYPE_INVALID_POST    = (-810),
    DWC_ECODE_TYPE_REQ_INVALID     = (-820),
    DWC_ECODE_TYPE_UNSPECIFIED     = (-830),
    DWC_ECODE_TYPE_BUFF_OVER       = (-840),
    DWC_ECODE_TYPE_PARSE_URL       = (-850),
    DWC_ECODE_TYPE_BAD_RESPONSE    = (-860),
    DWC_ECODE_TYPE_REJECTED        = (-870),
    DWC_ECODE_TYPE_FILE_RW         = (-880),
    DWC_ECODE_TYPE_INCOMPLETE      = (-890),
    DWC_ECODE_TYPE_TO_BIG          = (-900),
    DWC_ECODE_TYPE_ENCRYPTION      = (-910),
    DWC_ECODE_TYPE_ALLOC           = (-1),
    DWC_ECODE_TYPE_PARAM           = (-2),
    DWC_ECODE_TYPE_SO_SOCKET       = (-3),
    DWC_ECODE_TYPE_NOT_INIT        = (-4),
    DWC_ECODE_TYPE_DUP_INIT        = (-5),
    DWC_ECODE_TYPE_WM_INIT         = (-6),
    DWC_ECODE_TYPE_UNEXPECTED      = (-9),
    DWC_ECODE_SEQ_ADDINS           = (-30000),
    DWC_ECODE_FUNC_ND              = (-1000),
    DWC_ECODE_FUNC_PROF            = (-3000),
    DWC_ECODE_TYPE_ND_ALLOC        = (-1),
    DWC_ECODE_TYPE_ND_FATAL        = (-9),
    DWC_ECODE_TYPE_ND_BUSY         = (-10),
    DWC_ECODE_TYPE_ND_HTTP         = (-20),
    DWC_ECODE_TYPE_ND_BUFFULL      = (-30),
    DWC_ECODE_TYPE_ND_SERVER       = (0),
    DWC_ECODE_TYPE_PROF_CONN       = (-10),
    DWC_ECODE_TYPE_PROF_PARSE      = (-20),
    DWC_ECODE_TYPE_PROF_OTHER      = (-30)
};
typedef enum _GPResult {
    GP_NO_ERROR,
    GP_MEMORY_ERROR,
    GP_PARAMETER_ERROR,
    GP_NETWORK_ERROR,
    GP_SERVER_ERROR
} GPResult;
typedef enum
{
	GT2Success,             
                            
	GT2OutOfMemory,         
	GT2Rejected,            
	GT2NetworkError,        
	GT2AddressError,        
	GT2DuplicateAddress,    
	GT2TimedOut,			
	GT2NegotiationError,	
	GT2InvalidConnection,	
	GT2InvalidMessage,		
	GT2SendFailed			
} GT2Result;
#define DWC_STATE_LOGIN 2
#define DWC_LOGIN_STATE_REMOTE_AUTH 1
void DWCi_StopMatching(DWCError,int),DWCi_StopFriendProcess(DWCError,int);

GPResult native_main_0209becc (GPResult result);

GT2Result native_main_0209bf8c (GT2Result result);
