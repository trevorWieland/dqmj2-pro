#define DWCi_ClearQR2Key native_fn_0209f1c0
#define DWCi_SetState native_fn_0209be60
#define DWCi_GetAIDBitmapFromList native_fn_0209beac
#define DWCi_SetNumValidConnection native_fn_0209f640
typedef unsigned char u8;typedef unsigned short u16;typedef unsigned long u32;typedef unsigned long long u64;typedef u64 OSTick;typedef volatile u8 vu8;typedef int BOOL;typedef int GPResult;typedef int DWCError;typedef int SBError;typedef int SBState;typedef int NegotiateError;typedef int NegotiateResult;typedef int SOCKET;typedef int GT2Result;typedef unsigned char GT2Byte;typedef void*GT2Socket;typedef void*GT2Connection;typedef void*GPConnection;typedef void*qr2_t;typedef void*ServerBrowser;typedef void*SBServer;typedef struct{void*connected,*received,*closed,*ping;}GT2ConnectionCallbacks;typedef union{u32 words[3];}DWCFriendData;typedef void(*DWCMatchedSCCallback)(DWCError,BOOL,BOOL,BOOL,int,void*);typedef void(*DWCNewClientCallback)(int,void*);typedef int(*DWCEvalPlayerCallback)(int,void*);typedef void(*DWCStopSCCallback)(void*);struct sockaddr_in;
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
#define DWC_QR2_PID_KEY_STR                "dwc_pid"
#define DWC_QR2_MATCH_TYPE_KEY_STR         "dwc_mtype"
#define DWC_QR2_MATCH_RESV_KEY_STR         "dwc_mresv"
#define DWC_QR2_MATCH_VER_KEY_STR          "dwc_mver"
#define DWC_QR2_MATCH_EVAL_KEY_STR         "dwc_eval"
#define DWC_QR2_RESERVED_KEYS              (100 - NUM_RESERVED_KEYS)
#define DWC_QR2_GAME_RESERVED_KEYS         (MAX_REGISTERED_KEYS - NUM_RESERVED_KEYS - DWC_QR2_RESERVED_KEYS)
#define DWC_QR2_GAME_KEY_START              100
#define DWC_SB_COMMAND_STRING              "SBCM"
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
DWCMatchControl*DWCi_GetMatchCnt(void);BOOL DWCi_IsError(void);OSTick OS_GetTick(void);int DWC_GetState(void);void qr2_think(qr2_t),gt2Think(GT2Socket);SBError ServerBrowserThink(ServerBrowser);SBState ServerBrowserState(ServerBrowser);void ServerBrowserFree(ServerBrowser);void NNThink(void),NNFreeNegotiateList(void);GT2Result gt2Connect(GT2Socket,GT2Connection*,const char*,const GT2Byte*,int,int,GT2ConnectionCallbacks*);void DWCi_StopMatching(DWCError,int);GPResult DWCi_GPSetServerStatus(void);
BOOL DWCi_CancelPreConnectedClientProcess(int),DWCi_CancelPreConnectedServerProcess(int),DWCi_RetryReserving(int);int DWCi_HandleMatchCommandError(int),DWCi_ResumeMatching(void),DWCi_SendMatchCommand(u8,int,u32,u16,const u32[],int),DWCi_SendResvCommand(int,BOOL);SBError DWCi_HandleSBError(SBError),DWCi_SBUpdateAsync(int);void DWCi_NNCompletedCallback(NegotiateResult,SOCKET,struct sockaddr_in*,void*),DWCi_ProcessOptMinComp(void),DWCi_RestartFromTimeout(void),DWCi_SendStateChanged(qr2_t),DWCi_StopResendingMatchCommand(void);BOOL DWCi_ProcessMatchSynTimeout(void),DWCi_ProcessCancelMatchSynTimeout(void);
extern int native_data_021d1b88[7];
#define s_sbCallbackLevel native_data_021d1b88[6]
#define s_needSbFree native_data_021d1b88[5]
#define s_bInNNThink native_data_021d1b88[4]
#define s_bNNFreeNegotiateList native_data_021d1b88[3]
void native_main_0209e488(BOOL);

#define nr_deadbeatpartner 1
#define sb_disconnected 0

typedef int DWCState;typedef void(*DWCLoginCallback)(int,int,void*);typedef void(*DWCUpdateServersCallback)(int,BOOL,void*);typedef void(*DWCMatchedCallback)(int,BOOL,void*);typedef void(*DWCMatchedSCCallback)(int,BOOL,BOOL,BOOL,int,void*);typedef void(*DWCConnectionClosedCallback)(int,BOOL,BOOL,u8,int,void*);
typedef struct{void*gt2Socket;GT2ConnectionCallbacks gt2Callbacks;int gt2SendBufSize,gt2RecvBufSize;void*gpObj,*userdata;DWCState state,lastState;u8 aid,ownCloseFlag;u16 playerName[26];int profileID;const char*gameName,*secretKey;DWCLoginCallback loginCallback;void*loginParam;DWCUpdateServersCallback updateServersCallback;void*updateServersParam;DWCMatchedCallback matchedCallback;void*matchedParam;DWCMatchedSCCallback matchedSCCallback;void*matchedSCParam;DWCConnectionClosedCallback closedCallback;void*closedParam;u8 logcnt[640],friendcnt[96];DWCMatchControl matchcnt;}DWCCorePrefix;
extern DWCCorePrefix*native_data_021d19e0;
#define stpDwcCnt native_data_021d19e0
#define SDK_FINALROM 1
#define DWC_ERROR_NONE 0
#define DWC_STATE_ONLINE 3
#define DWC_STATE_CONNECTED 6
void DWCi_ClearQR2Key(void),DWCi_SetState(DWCState),DWCi_SetNumValidConnection(void);u32 DWCi_GetAIDBitmapFromList(u8*,int);
void native_main_0209c05c (DWCError error, BOOL cancel, BOOL self, BOOL isServer, int index, void * param);
