typedef enum{nr_success,nr_deadbeatpartner,nr_inittimeout,nr_pingtimeout,nr_unknownerror,nr_noresult}NegotiateResult;
typedef enum{ne_noerror,ne_allocerror,ne_socketerror,ne_dnserror}NegotiateError;
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef u64 OSTick;typedef volatile u8 vu8;typedef int BOOL;typedef int GPResult;typedef int DWCError;typedef int SBError;typedef int SBState;typedef int SOCKET;typedef int GT2Result;typedef unsigned char GT2Byte;typedef struct GTI2Socket*GT2Socket;typedef void*GT2Connection;typedef void*GPConnection;typedef void*qr2_t;typedef struct _ServerBrowser*ServerBrowser;typedef struct _SBServer*SBServer;typedef struct{void*connected,*received,*closed,*ping;}GT2ConnectionCallbacks;typedef union{u32 words[3];}DWCFriendData;typedef void(*DWCMatchedSCCallback)(DWCError,BOOL,BOOL,BOOL,int,void*);typedef void(*DWCNewClientCallback)(int,void*);typedef int(*DWCEvalPlayerCallback)(int,void*);typedef void(*DWCStopSCCallback)(void*);struct sockaddr_in;
#define NULL ((void*)0)
#define TRUE 1
#define FALSE 0
#define SDK_ASSERT(x) ((void)0)
#define DWC_Printf(...) ((void)0)
#define DWC_STATE_MATCHING 5
#define DWC_ERROR_NETWORK 6
#define DWC_ECODE_SEQ_MATCH (-80000)
#define DWC_ECODE_GS_SB (-5000)
#define DWC_ECODE_TYPE_NETWORK (-10)
#define DWC_ECODE_TYPE_SC_CL_FAIL (-430)
#define DWC_MATCH_CANCEL_STATE_INIT 0
#define OS_MilliSecondsToTicks(m) ((OSTick)((33514*(u64)(m))/64))
#define OS_TicksToMilliSeconds(t) (((u64)(t)*64)/33514)
#define DWC_QR2_ALIVE_DURING_MATCHING
#define DWC_MATCH_ACCEPT_NO_FRIEND
#define DWC_LIMIT_FRIENDS_MATCH_VALID
#define DWC_STOP_SC_SERVER
#define DWC_MATCHING_VERSION    3U
#define DWC_MAX_CONNECTIONS     32
#define DWC_QR2_PID_KEY                     NUM_RESERVED_KEYS
#define DWC_QR2_MATCH_TYPE_KEY             (NUM_RESERVED_KEYS + 1)
#define DWC_QR2_MATCH_RESV_KEY             (NUM_RESERVED_KEYS + 2)
#define DWC_QR2_MATCH_VER_KEY              (NUM_RESERVED_KEYS + 3)
#define DWC_QR2_MATCH_EVAL_KEY             (NUM_RESERVED_KEYS + 4)
#define DWC_QR2_PID_KEY_STR                native_data_020e01f4
#define DWC_QR2_MATCH_TYPE_KEY_STR         "dwc_mtype"
#define DWC_QR2_MATCH_RESV_KEY_STR         "dwc_mresv"
#define DWC_QR2_MATCH_VER_KEY_STR          "dwc_mver"
#define DWC_QR2_MATCH_EVAL_KEY_STR         "dwc_eval"
#define DWC_QR2_RESERVED_KEYS              (100 - NUM_RESERVED_KEYS)
#define DWC_QR2_GAME_RESERVED_KEYS         (MAX_REGISTERED_KEYS - NUM_RESERVED_KEYS - DWC_QR2_RESERVED_KEYS)
#define DWC_QR2_GAME_KEY_START              100
#define DWC_SB_COMMAND_STRING              native_data_020e029c
#define DWC_MATCH_COMMAND_RESERVATION       0x01
#define DWC_MATCH_COMMAND_RESV_OK           0x02
#define DWC_MATCH_COMMAND_RESV_DENY         0x03
#define DWC_MATCH_COMMAND_RESV_WAIT         0x04
#define DWC_MATCH_COMMAND_RESV_CANCEL       0x05
#define DWC_MATCH_COMMAND_TELL_ADDR         0x06
#define DWC_MATCH_COMMAND_NEW_PID_AID       0x07
#define DWC_MATCH_COMMAND_LINK_CLS_REQ      0x08
#define DWC_MATCH_COMMAND_LINK_CLS_SUC      0x09
#define DWC_MATCH_COMMAND_CLOSE_LINK        0x0a
#define DWC_MATCH_COMMAND_RESV_PRIOR        0x0b
#define DWC_MATCH_COMMAND_CANCEL            0x0c
#define DWC_MATCH_COMMAND_CANCEL_SYN        0x0d
#define DWC_MATCH_COMMAND_CANCEL_SYN_ACK    0x0e
#define DWC_MATCH_COMMAND_CANCEL_ACK        0x0f
#define DWC_MATCH_COMMAND_SC_CLOSE_CL       0x10
#define DWC_MATCH_COMMAND_POLL_TIMEOUT      0x11
#define DWC_MATCH_COMMAND_POLL_TO_ACK       0x12
#define DWC_MATCH_COMMAND_SC_CONN_BLOCK     0x13
#define DWC_MATCH_COMMAND_CL_WAIT_POLL      0x40
#define DWC_MATCH_COMMAND_SV_KA_TO_CL       0x41
#define DWC_MATCH_COMMAND_DUMMY             0xff
#define DWC_MATCH_CMD_RESEND_INTERVAL_MSEC        3000
#define DWC_MATCH_CMD_RESEND_INTERVAL_ADD_MSEC    3000
#define DWC_MATCH_CMD_RESV_TIMEOUT_MSEC           6000
#define DWC_SB_UPDATE_INTERVAL_MSEC               3000
#define DWC_SB_UPDATE_INTERVAL_SHORT_MSEC         1000
#define DWC_SB_UPDATE_INTERVAL_ADD_MSEC           3000
#define DWC_SB_UPDATE_INTERVAL_SHORT              1
#define DWC_SB_UPDATE_INTERVAL_LONG               2
#define DWC_SB_UPDATE_TIMEOUT                     30000
#define DWC_MATCH_CMD_RTT_TIMEOUT                 6000
#define DWC_MATCH_SB_UPDATE_TIMEOUT               13000
#define DWC_MATCH_CMD_RETRY_MAX                   5
#define DWC_MATCH_SYN_ACK_WAIT_TIME           DWC_MATCH_CMD_RTT_TIMEOUT
#define DWC_MATCH_CANCEL_SYN_ACK_WAIT_TIME    DWC_MATCH_CMD_RTT_TIMEOUT
#define DWC_MATCH_RESV_KEEP_TIME_ANYBODY      DWC_MATCH_CMD_RTT_TIMEOUT
#define DWC_MATCH_RESV_KEEP_TIME_FRIEND      (DWC_MATCH_CMD_RTT_TIMEOUT + DWC_MATCH_SB_UPDATE_TIMEOUT)
#define DWC_MAX_MATCH_NN_RETRY                   1
#define DWC_MATCH_NN_FAILURE_MAX                 5
#define DWC_WAIT_NN_RETRY_TIMEOUT                10000
#define DWC_GT2_CONNECT_TIMEOUT                  5000
#define DWC_WAIT_GT2_CONNECT_TIMEOUT            (DWC_GT2_CONNECT_TIMEOUT * DWC_MATCH_CMD_RETRY_MAX)
#define DWC_MATCH_LINK_CLS_TIMEOUT               30000
#define DWC_MATCH_CL_WAIT_TIMEOUT                30000
#define DWC_RESV_COMMAND_RETRY_MAX               16
#define DWC_MATCH_OPT_MIN_COMP_POLL_RETRY_MAX    5
#define DWC_SB_UPDATE_MAX_SERVERS                6
#define DWC_MATCH_SYN_DATA_BODY_SIZE             4
#define DWC_MAX_MATCH_IDX_LIST                   64
typedef enum {
    DWC_MATCH_OPTION_MIN_COMPLETE = 0,
    DWC_MATCH_OPTION_SC_CONNECT_BLOCK,
    DWC_MATCH_OPTION_NUM
} DWCMatchOptType;
enum {
    DWC_SET_MATCH_OPT_RESULT_SUCCESS = 0,
    DWC_SET_MATCH_OPT_RESULT_E_BAD_STATE,
    DWC_SET_MATCH_OPT_RESULT_E_INVALID,
    DWC_SET_MATCH_OPT_RESULT_E_PARAM,
    DWC_SET_MATCH_OPT_RESULT_E_ALLOC,
    DWC_SET_MATCH_OPT_RESULT_NUM
};
typedef enum {
    DWC_MATCH_STATE_INIT = 0,
    DWC_MATCH_STATE_CL_WAITING,
    DWC_MATCH_STATE_CL_SEARCH_OWN,
    DWC_MATCH_STATE_CL_SEARCH_HOST,
    DWC_MATCH_STATE_CL_WAIT_RESV,
    DWC_MATCH_STATE_CL_SEARCH_NN_HOST,
    DWC_MATCH_STATE_CL_NN,
    DWC_MATCH_STATE_CL_GT2,
    DWC_MATCH_STATE_CL_CANCEL_SYN,
    DWC_MATCH_STATE_CL_SYN,
    DWC_MATCH_STATE_SV_WAITING,
    DWC_MATCH_STATE_SV_OWN_NN,
    DWC_MATCH_STATE_SV_OWN_GT2,
    DWC_MATCH_STATE_SV_WAIT_CL_LINK,
    DWC_MATCH_STATE_SV_CANCEL_SYN,
    DWC_MATCH_STATE_SV_CANCEL_SYN_WAIT,
    DWC_MATCH_STATE_SV_SYN,
    DWC_MATCH_STATE_SV_SYN_WAIT,
    DWC_MATCH_STATE_WAIT_CLOSE,
    DWC_MATCH_STATE_SV_POLL_TIMEOUT,
    DWC_MATCH_STATE_NUM
} DWCMatchState;
enum {
    DWC_MATCH_TYPE_ANYBODY = 0,
    DWC_MATCH_TYPE_FRIEND,
    DWC_MATCH_TYPE_SC_SV,
    DWC_MATCH_TYPE_SC_CL,
    DWC_MATCH_TYPE_NUM
};
typedef struct DWCstNNInfo {
    u8 isQR2;
    u8 retryCount;
    u16 port;
    u32 ip;
    int cookie;
} DWCNNInfo;
typedef struct DWCstMatchCommandControl {
    u8 command;
    u8 count;
    u16 port;
    u32 ip;
    u32 data[32];
    int profileID;
    int len;
    OSTick sendTime;
} DWCMatchCommandControl;
typedef struct DWCstMatchControl {
    GPConnection * pGpObj;
    GT2Socket * pGt2Socket;
    GT2ConnectionCallbacks * gt2Callbacks;
    u8 gt2ConnectCount;
    u8 gt2NumConnection;
    u8 gt2NumValidConn;
    u8 pad1;
    qr2_t qr2Obj;
    vu8 qr2NNFinishCount;
    vu8 qr2MatchType;
    vu8 qr2NumEntry;
    vu8 qr2IsReserved;
#ifdef DWC_QR2_ALIVE_DURING_MATCHING
    u8 qr2ShutdownFlag;
    u8 pad2;
#else
    u16 pad2;
#endif
    u16 qr2Port;
    u32 qr2IP;
    volatile int qr2Reservation;
    u32 qr2IPList[DWC_MAX_CONNECTIONS];
    u16 qr2PortList[DWC_MAX_CONNECTIONS];
    ServerBrowser sbObj;
    BOOL sbUpdateFlag;
    OSTick sbUpdateTick;
    int sbPidList[DWC_MAX_CONNECTIONS];
    OSTick sbUpdateRequestTick;
    u8 nnRecvCount;
    u8 nnFailureCount;
    u16 nnCookieRand;
    int nnLastCookie;
    OSTick nnFailedTime;
    OSTick nnFinishTime;
    DWCNNInfo nnInfo;
    DWCMatchState state;
    u8 clLinkProgress;
    u8 friendCount;
    u8 distantFriend;
    u8 resvWaitCount;
    u8 closeState;
    u8 cancelState;
    u8 scResvRetryCount;
    u8 synResendCount;
    u8 cancelSynResendCount;
    u8 clWaitTimeoutCount;
#ifdef DWC_STOP_SC_SERVER
    u8 stopSCFlag;
    u8 pad3;
#endif
    u16 baseLatency;
    u16 cancelBaseLatency;
    u16 searchPort;
#ifdef DWC_STOP_SC_SERVER
    u16 pad4;
#endif
    u32 searchIP;
    BOOL cmdResendFlag;
    OSTick cmdResendTick;
    u32 cmdTimeoutTime;
    OSTick cmdTimeoutStartTick;
    u32 synAckBit;
    u32 cancelSynAckBit;
#ifdef DWC_LIMIT_FRIENDS_MATCH_VALID
    u32 friendAcceptBit;
#endif
    OSTick lastSynSent;
    OSTick lastCancelSynSent;
    OSTick closedTime;
    OSTick clWaitTime;
    volatile int profileID;
    int reqProfileID;
    int priorProfileID;
    int cbEventPid;
    u32 ipList[DWC_MAX_CONNECTIONS];
    u16 portList[DWC_MAX_CONNECTIONS];
    u8 aidList[DWC_MAX_CONNECTIONS];
    u32 validAidBitmap;
    const char * gameName;
    const char * secretKey;
    const DWCFriendData * friendList;
    int friendListLen;
    u8 friendIdxList[DWC_MAX_MATCH_IDX_LIST];
    int friendIdxListLen;
    u32 svDataBak[DWC_MAX_CONNECTIONS + 1];
    DWCMatchCommandControl cmdCnt;
    DWCMatchedSCCallback matchedCallback;
    void * matchedParam;
    DWCNewClientCallback newClientCallback;
    void * newClientParam;
    DWCEvalPlayerCallback evalCallback;
    void * evalParam;
#ifdef DWC_STOP_SC_SERVER
    DWCStopSCCallback stopSCCallback;
    void * stopSCParam;
#endif
} DWCMatchControl;
typedef struct DWCstMatchOptMinCompleteIn {
    u8 valid;
    u8 minEntry;
    u8 retry;
    u8 pad;
    u32 timeout;
    u32 recvBit;
    u32 timeoutBit;
    OSTick startTime;
    OSTick lastPollTime;
} DWCMatchOptMinCompleteIn;
typedef struct DWCstMatchOptSCBlock {
    u8 valid;
    u8 lock;
    u16 pad;
} DWCMatchOptSCBlock;
#define NUM_RESERVED_KEYS 50
#define MAX_REGISTERED_KEYS 254
#define NUMPLAYERS_KEY 8
#define MAXPLAYERS_KEY 10
#define MAX_FILTER_LEN 256
#define DWC_NUM_QR2_MATCH_KEY 7
#define DWC_DNS_ERROR_RETRY_MAX 5
#define SBTrue 1
#define SBFalse 0
#define sbe_noerror 0
#define sbe_dnserror 2
typedef struct{u8 keyID,isStr;u16 pad;char*keyStr;const void*value;}DWCGameMatchKeyData;
extern DWCGameMatchKeyData stGameMatchKeys[DWC_QR2_GAME_RESERVED_KEYS];
typedef struct{u8 opaque[8];char*addFilter;}MatchGlobalsView;
extern MatchGlobalsView native_data_021d1b88;
#define stpAddFilter (native_data_021d1b88.addFilter)
extern DWCMatchControl*native_fn_020a3d70(void);
extern int DWCi_GetDefaultMatchFilter(char*,int,u8,u8);
extern int native_fn_020061ac(char*,u32,const char*,...);
extern void ServerBrowserClear(ServerBrowser);
extern SBError ServerBrowserLimitUpdate(ServerBrowser,BOOL,BOOL,const u8*,int,const char*,int);
extern OSTick native_fn_02007a9c(void);
extern void native_fn_02008c28(const void*,void*,u32);
#define ne_noerror 0
#define ne_socketerror 2
#define nr_success 0
extern BOOL SBServerHasPrivateAddress(SBServer);
extern u32 native_fn_020a60b0(SBServer),ServerBrowserGetMyPublicIPAddr(ServerBrowser),SBServerGetPrivateInetAddress(SBServer),SO_GetHostID(void);
extern u16 SBServerGetPrivateQueryPort(SBServer),native_fn_020a60b4(SBServer),gt2GetLocalPort(GT2Socket);
extern u32 DWCi_GetMathRand32(u32);
extern int native_fn_020a00ac(u8,int,u32,u16,const u32*,int);
extern NegotiateError DWCi_DoNatNegotiationAsync(DWCNNInfo*);
extern SOCKET gt2GetSocketSOCKET(GT2Socket);
extern void DWCi_NNCompletedCallback(NegotiateResult,SOCKET,struct sockaddr_in*,void*);
extern SBServer native_fn_020a699c(ServerBrowser,int);
extern int native_fn_020a601c(SBServer,const char*,int);
#define DWC_MATCH_COMMAND_ADD_MESSAGE_MAX 512
#define SDK_ASSERTMSG(...)
typedef char gsi_char;
typedef struct{char identifier[4];u32 version;u8 command,size;u16 qr2Port;u32 qr2IP;int profileID;}DWCSBMessageHeader;
typedef struct{DWCSBMessageHeader header;u32 data[32];}DWCSBMessage;
#include "string.h"
extern char*native_fn_020b5f38(u32,u16,char*);
extern SBError native_fn_020a68b4(ServerBrowser,const char*,u16,const char*,int);
extern SBError native_fn_020a020c(u8,u32,u16,const u32*,int);
extern GPResult native_fn_020a02b4(GPConnection*,u8,int,const char*);
extern void native_fn_02008e0c(const void*,void*,u32);
extern void native_fn_020b748c(qr2_t);
extern const char native_data_020e01a4[];
extern const char native_data_020e01f4[];
extern const char native_data_020e0298[];
extern const char native_data_020e029c[];
SBError native_main_020a020c (u8 command, u32 ip, u16 port, const u32 data[], int len)
;
