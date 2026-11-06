typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed char s8;
typedef signed long s32;
typedef int BOOL;
void native_fn_02008430();
extern void native_fn_02008430(void);
extern void native_fn_02008064(u32 cycle);
typedef struct CPContext {
	u64 div_numer;
	u64 div_denom;
	u64 sqrt;
	u16 div_mode;
	u16 sqrt_mode;
} CPContext;
typedef struct OSContext {
	u32 cpsr;
	u32 r[13];
	u32 sp;
	u32 lr;
	u32 pc_plus4;
	u32 sp_svc;
	CPContext cp_context;
} OSContext;
typedef struct _OSThread OSThread;
typedef struct _OSThreadQueue OSThreadQueue;
typedef struct _OSThreadLink OSThreadLink;
typedef struct _OSMutexQueue OSMutexQueue;
typedef struct _OSMutexLink OSMutexLink;
typedef struct OSMutex OSMutex;
typedef struct OSiAlarm OSAlarm;
struct _OSThreadQueue {
        OSThread * head;
        OSThread * tail;
    };
struct _OSThreadLink {
        OSThread * prev;
        OSThread * next;
    };
struct _OSMutexQueue {
        OSMutex * head;
        OSMutex * tail;
    };
struct _OSMutexLink {
        OSMutex * next;
        OSMutex * prev;
    };
typedef enum {
    OS_THREAD_STATE_WAITING       = 0,
    OS_THREAD_STATE_READY         = 1,
    OS_THREAD_STATE_TERMINATED    = 2
} OSThreadState;
typedef void (*OSThreadDestructor) (void *);
struct _OSThread {
    OSContext context;
    OSThreadState state;
    OSThread * next;
    u32 id;
    u32 priority;
    void * profiler;
    OSThreadQueue * queue;
    OSThreadLink link;
    OSMutex * mutex;
    OSMutexQueue mutexQueue;
    u32 stackTop;
    u32 stackBottom;
    u32 stackWarningOffset;
    OSThreadQueue joinQueue;
    void * specific[3 ];
    OSAlarm * alarmForSleep;
    OSThreadDestructor destructor;
    void * userParameter;
    int systemErrno;
};
struct OSMutex {
	OSThreadQueue queue;
	OSThread * thread;
	s32 count;
	OSMutexLink link;
};
typedef u64 OSTick;
typedef void (*OSAlarmHandler) (void *);
struct OSiAlarm {
	OSAlarmHandler handler;
	void * arg;
	u32 tag;
	OSTick fire;
	OSAlarm * prev;
	OSAlarm * next;
	OSTick period;
	OSTick start;
};
typedef enum WMApiid {
	WM_APIID_INITIALIZE = 0,
	WM_APIID_RESET,
	WM_APIID_END,
	WM_APIID_ENABLE,
	WM_APIID_DISABLE,
	WM_APIID_POWER_ON,
	WM_APIID_POWER_OFF,
	WM_APIID_SET_P_PARAM,
	WM_APIID_START_PARENT,
	WM_APIID_END_PARENT,
	WM_APIID_START_SCAN,
	WM_APIID_END_SCAN,
	WM_APIID_START_CONNECT,
	WM_APIID_DISCONNECT,
	WM_APIID_START_MP,
	WM_APIID_SET_MP_DATA,
	WM_APIID_END_MP,
	WM_APIID_START_DCF,
	WM_APIID_SET_DCF_DATA,
	WM_APIID_END_DCF,
	WM_APIID_SET_WEPKEY,
	WM_APIID_START_KS,
	WM_APIID_END_KS,
	WM_APIID_GET_KEYSET,
	WM_APIID_SET_GAMEINFO,
	WM_APIID_SET_BEACON_IND,
	WM_APIID_START_TESTMODE,
	WM_APIID_STOP_TESTMODE,
	WM_APIID_VALARM_MP,
	WM_APIID_SET_LIFETIME,
	WM_APIID_MEASURE_CHANNEL,
	WM_APIID_INIT_W_COUNTER,
	WM_APIID_GET_W_COUNTER,
	WM_APIID_SET_ENTRY,
	WM_APIID_AUTO_DEAUTH,
	WM_APIID_SET_MP_PARAMETER,
	WM_APIID_SET_BEACON_PERIOD,
	WM_APIID_AUTO_DISCONNECT,
	WM_APIID_START_SCAN_EX,
	WM_APIID_SET_WEPKEY_EX,
	WM_APIID_SET_PS_MODE,
	WM_APIID_START_TESTRXMODE,
	WM_APIID_STOP_TESTRXMODE,
	WM_APIID_KICK_MP_PARENT,
	WM_APIID_KICK_MP_CHILD,
	WM_APIID_KICK_MP_RESUME,
	WM_APIID_ASYNC_KIND_MAX,
	WM_APIID_INDICATION = 128,
	WM_APIID_PORT_SEND,
	WM_APIID_PORT_RECV,
	WM_APIID_READ_STATUS,
	WM_APIID_UNKNOWN = 255
} WMApiid;
typedef enum WMPort {
	WM_PORT_RAWDATA = 0,
	WM_PORT_BT = 1,
	WM_PORT_RESERVE_02 = 2,
	WM_PORT_RESERVE_03 = 3,
	WM_PORT_RESERVE_10 = 8,
	WM_PORT_RESERVE_11 = 9,
	WM_PORT_RESERVE_12 = 10,
	WM_PORT_RESERVE_13 = 11
} WMPort;
typedef enum WMErrCode {
	WM_ERRCODE_SUCCESS               = 0,
	WM_ERRCODE_FAILED                = 1,
	WM_ERRCODE_OPERATING             = 2,
	WM_ERRCODE_ILLEGAL_STATE         = 3,
	WM_ERRCODE_WM_DISABLE            = 4,
	WM_ERRCODE_NO_KEYSET             = 5,
	WM_ERRCODE_NO_DATASET            = 5,
	WM_ERRCODE_INVALID_PARAM         = 6,
	WM_ERRCODE_NO_CHILD              = 7,
	WM_ERRCODE_FIFO_ERROR            = 8,
	WM_ERRCODE_TIMEOUT               = 9,
	WM_ERRCODE_SEND_QUEUE_FULL       = 10,
	WM_ERRCODE_NO_ENTRY              = 11,
	WM_ERRCODE_OVER_MAX_ENTRY        = 12,
	WM_ERRCODE_INVALID_POLLBITMAP    = 13,
	WM_ERRCODE_NO_DATA               = 14,
	WM_ERRCODE_SEND_FAILED           = 15,
	WM_ERRCODE_DCF_TEST,
	WM_ERRCODE_WL_INVALID_PARAM,
	WM_ERRCODE_WL_LENGTH_ERR,
	WM_ERRCODE_FLASH_ERROR,
	WM_ERRCODE_MAX
} WMErrCode;
typedef enum WMStateCode {
	WM_STATECODE_PARENT_START                = 0,
	WM_STATECODE_BEACON_SENT                 = 2,
	WM_STATECODE_SCAN_START                  = 3,
	WM_STATECODE_PARENT_NOT_FOUND            = 4,
	WM_STATECODE_PARENT_FOUND                = 5,
	WM_STATECODE_CONNECT_START               = 6,
	WM_STATECODE_BEACON_LOST                 = 8,
	WM_STATECODE_CONNECTED                   = 7,
	WM_STATECODE_CHILD_CONNECTED             = 7,
	WM_STATECODE_DISCONNECTED                = 9,
	WM_STATECODE_DISCONNECTED_FROM_MYSELF    = 26,
	WM_STATECODE_MP_START                    = 10,
	WM_STATECODE_MPEND_IND                   = 11,
	WM_STATECODE_MP_IND                      = 12,
	WM_STATECODE_MPACK_IND                   = 13,
	WM_STATECODE_DCF_START                   = 14,
	WM_STATECODE_DCF_IND                     = 15,
	WM_STATECODE_BEACON_RECV                 = 16,
	WM_STATECODE_DISASSOCIATE                = 17,
	WM_STATECODE_REASSOCIATE                 = 18,
	WM_STATECODE_AUTHENTICATE                = 19,
	WM_STATECODE_PORT_INIT                   = 25,
	WM_STATECODE_PORT_SEND                   = 20,
	WM_STATECODE_PORT_RECV                   = 21,
	WM_STATECODE_FIFO_ERROR                  = 22,
	WM_STATECODE_INFORMATION                 = 23,
	WM_STATECODE_UNKNOWN                     = 24,
	WM_STATECODE_MAX                         = 27
} WMStateCode;
typedef void (*WMCallbackFunc) (void * arg);
typedef struct WMMpRecvBuf {
	u16 rsv1[3];
	u16 length;
	u16 rsv2[1];
	u16 ackTimeStamp;
	u16 timeStamp;
	u16 rate_rssi;
	u16 rsv3[2];
	u16 rsv4[2];
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 rsv5[3];
	u16 seqCtrl;
	u16 txop;
	u16 bitmap;
	u16 wmHeader;
	u16 data[2];
} WMMpRecvBuf, WMmpRecvBuf;
typedef struct WMParentParam {
	u16 * userGameInfo;
	u16 userGameInfoLength;
	u16 padding;
	u32 ggid;
	u16 tgid;
	u16 entryFlag;
	u16 maxEntry;
	u16 multiBootFlag;
	u16 KS_Flag;
	u16 CS_Flag;
	u16 beaconPeriod;
	u16 rsv1[8 / sizeof(u16)];
	u16 rsv2[16 / sizeof(u16)];
	u16 channel;
	u16 parentMaxSize;
	u16 childMaxSize;
	u16 rsv[4];
} WMParentParam, WMpparam;
typedef struct WMGameInfo {
	u16 magicNumber;
	u8 ver;
	u8 platform;
	u32 ggid;
	u16 tgid;
	u8 userGameInfoLength;
	union {
		u8 gameNameCount_attribute;
		u8 attribute;
	};
	u16 parentMaxSize;
	u16 childMaxSize;
	union {
		u16 userGameInfo[112 / sizeof(u16)];
		struct {
			u16 userName[8 / sizeof(u16)];
			u16 gameName[16 / sizeof(u16)];
			u16 padd1[44];
		} old_type;
	};
} WMGameInfo, WMgameInfo;
typedef struct WMBssDesc {
        u16 length;
        u16 rssi;
        u8 bssid[6 ];
        u16 ssidLength;
        u8 ssid[32 ];
        u16 capaInfo;
        struct {
            u16 basic;
            u16 support;
        } rateSet;
        u16 beaconPeriod;
        u16 dtimPeriod;
        u16 channel;
        u16 cfpPeriod;
        u16 cfpMaxDuration;
        u16 gameInfoLength;
        u16 otherElementCount;
        WMGameInfo gameInfo;
    } WMBssDesc, WMbssDesc;
typedef struct WMScanParam {
	WMBssDesc * scanBuf;
	u16 channel;
	u16 maxChannelTime;
	u8 bssid[6 ];
	u16 rsv[9];
} WMScanParam, WMscanParam;
typedef struct WMCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
} WMCallback;
typedef struct WMStartParentCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u8 macAddress[6 ];
	u16 aid;
	u16 reason;
	u8 ssid[24 ];
	u16 parentSize;
	u16 childSize;
} WMStartParentCallback, WMstartParentCallback;
typedef struct WMStartScanCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u8 macAddress[6 ];
	u16 channel;
	u16 linkLevel;
	u16 ssidLength;
	u16 ssid[32 / sizeof(u16)];
	u16 gameInfoLength;
	WMGameInfo gameInfo;
} WMStartScanCallback, WMstartScanCallback;
typedef struct WMDisconnectCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 tryBitmap;
	u16 disconnectedBitmap;
} WMDisconnectCallback;
typedef struct WMStartMPCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u8 reserved[2];
	WMMpRecvBuf * recvBuf;
	u16 timeStamp;
	u16 rate_rssi;
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 seqNum;
	u16 tmptt;
	u16 pollbmp;
	u16 reserved2;
} WMStartMPCallback, WMstartMPCallback;
typedef struct WMIndCallback {
	u16 apiid;
	u16 errcode;
	u16 state;
	u16 reason;
} WMIndCallback, WMindCallback;
WMErrCode native_fn_02011f14(WMCallbackFunc callback);
WMErrCode native_fn_02011f58(u16 port, WMCallbackFunc callback, void * arg);
WMErrCode native_fn_02012824(WMCallbackFunc callback);
WMErrCode native_fn_02012864(WMCallbackFunc callback, const WMParentParam * pparaBuf);
WMErrCode native_fn_02012990(WMCallbackFunc callback, BOOL powerSave);
WMErrCode native_fn_02012fdc(WMCallbackFunc callback,
                       u16 * recvBuf,
                       u16 recvBufSize,
                       u16 * sendBuf,
                       u16 sendBufSize,
                       u16 mpFreq,
                       u16 defaultRetryCount,
                       BOOL minPollBmpMode,
                       BOOL singlePacketMode, BOOL fixFreqMode, BOOL ignoreFatalError);
WMErrCode native_fn_020141b0(WMCallbackFunc callback, u16 flag);
enum {
	FS_ARCHIVE_NAME_LEN_MAX = 3
};
typedef enum {
	FS_COMMAND_ASYNC_BEGIN = 0,
	FS_COMMAND_READFILE = FS_COMMAND_ASYNC_BEGIN,
	FS_COMMAND_WRITEFILE,
	FS_COMMAND_ASYNC_END,
	FS_COMMAND_SYNC_BEGIN = FS_COMMAND_ASYNC_END,
	FS_COMMAND_SEEKDIR = FS_COMMAND_SYNC_BEGIN,
	FS_COMMAND_READDIR,
	FS_COMMAND_FINDPATH,
	FS_COMMAND_GETPATH,
	FS_COMMAND_OPENFILEFAST,
	FS_COMMAND_OPENFILEDIRECT,
	FS_COMMAND_CLOSEFILE,
	FS_COMMAND_SYNC_END,
	FS_COMMAND_STATUS_BEGIN = FS_COMMAND_SYNC_END,
	FS_COMMAND_ACTIVATE = FS_COMMAND_STATUS_BEGIN,
	FS_COMMAND_IDLE,
	FS_COMMAND_SUSPEND,
	FS_COMMAND_RESUME,
	FS_COMMAND_STATUS_END,
	FS_COMMAND_INVALID
} FSCommandType;
typedef enum {
	FS_RESULT_SUCCESS = 0,
	FS_RESULT_FAILURE,
	FS_RESULT_BUSY,
	FS_RESULT_CANCELED,
	FS_RESULT_CANCELLED = FS_RESULT_CANCELED,
	FS_RESULT_UNSUPPORTED,
	FS_RESULT_ERROR,
	FS_RESULT_PROC_ASYNC,
	FS_RESULT_PROC_DEFAULT,
	FS_RESULT_PROC_UNKNOWN
} FSResult;
struct FSFile;
struct FSFileLink;
struct FSArchive;
typedef FSResult (*FS_ARCHIVE_PROC_FUNC) (struct FSFile *, FSCommandType);
typedef FSResult (*FS_ARCHIVE_READ_FUNC) (struct FSArchive * p, void * dst, u32 pos, u32 size);
typedef FSResult (*FS_ARCHIVE_WRITE_FUNC) (struct FSArchive * p, const void * src, u32 pos, u32 size);
typedef struct FSFileLink {
	struct FSFile * prev;
	struct FSFile * next;
} FSFileLink;
typedef struct FSArchive {
	union {
		char ptr[FS_ARCHIVE_NAME_LEN_MAX + 1];
		u32 pack;
	} name;
	struct FSArchive * next;
	struct FSArchive * prev;
	OSThreadQueue sync_q;
	OSThreadQueue stat_q;
	u32 flag;
	FSFileLink list;
	u32 base;
	u32 fat;
	u32 fat_size;
	u32 fnt;
	u32 fnt_size;
	u32 fat_bak;
	u32 fnt_bak;
	void * load_mem;
	FS_ARCHIVE_READ_FUNC read_func;
	FS_ARCHIVE_WRITE_FUNC write_func;
	FS_ARCHIVE_READ_FUNC table_func;
	FS_ARCHIVE_PROC_FUNC proc;
	u32 proc_flag;
} FSArchive;
struct FSFile;
typedef struct {
	struct FSArchive * arc;
	u16 own_id;
	u16 index;
	u32 pos;
} FSDirPos;
typedef struct {
	struct FSArchive * arc;
	u32 file_id;
} FSFileID;
typedef struct {
	union {
		FSFileID file_id;
		FSDirPos dir_id;
	};
	u32 is_directory;
	u32 name_len;
	char name[127 + 1];
} FSDirEntry;
typedef struct {
	FSDirPos pos;
} FSSeekDirInfo;
typedef struct {
	FSDirEntry * p_entry;
	BOOL skip_string;
} FSReadDirInfo;
