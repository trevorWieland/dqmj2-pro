typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef unsigned long long int u64;

typedef signed short int s16;

typedef signed long s32;

typedef int BOOL;

typedef struct OSContext {
	u32 cpsr;
	u32 r[13];
	u32 sp;
	u32 lr;
	u32 pc_plus4;
	u32 sp_svc;
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

typedef struct OSMessageQueue OSMessageQueue;

typedef void * OSMessage;

struct OSMessageQueue {
	OSThreadQueue queueSend;
	OSThreadQueue queueReceive;
	OSMessage * msgArray;
	s32 msgCount;
	s32 firstIndex;
	s32 usedCount;
};

struct OSMutex {
	OSThreadQueue queue;
	OSThread * thread;
	s32 count;
	OSMutexLink link;
};

typedef enum {
	OS_ARENA_MAIN            = 0,
	OS_ARENA_MAIN_SUBPRIV    = 1,
	OS_ARENA_MAINEX          = 2,
	OS_ARENA_ITCM            = 3,
	OS_ARENA_DTCM            = 4,
	OS_ARENA_SHARED          = 5,
	OS_ARENA_WRAM_MAIN       = 6,
	OS_ARENA_WRAM_SUB        = 7,
	OS_ARENA_WRAM_SUBPRIV    = 8,
	OS_ARENA_MAX             = 9
} OSArenaId;

typedef int OSHeapHandle;

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

typedef enum WMState {
	WM_STATE_READY = 0,
	WM_STATE_STOP,
	WM_STATE_IDLE,
	WM_STATE_CLASS1,
	WM_STATE_TESTMODE,
	WM_STATE_SCAN,
	WM_STATE_CONNECT,
	WM_STATE_PARENT,
	WM_STATE_CHILD,
	WM_STATE_MP_PARENT,
	WM_STATE_MP_CHILD,
	WM_STATE_DCF_CHILD,
	WM_STATE_TESTMODE_RX,
	WM_STATE_MAX
} WMState;

typedef void (*WMCallbackFunc) (void * arg);

typedef struct {
	u16 next;
	u16 port;
	u16 destBitmap;
	u16 restBitmap;
	u16 sentBitmap;
	u16 sendingBitmap;
	u16 padding;
	u16 size;
	u16 seqNo;
	u16 retryCount;
	const u16 * data;
	WMCallbackFunc callback;
	void * arg;
} WMPortSendQueueData;

typedef struct {
	u16 head;
	u16 tail;
} WMPortSendQueue;

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

typedef struct WMDcfRecvBuf {
	u16 frameID;
	u16 rsv1[2];
	u16 length;
	u16 rsv2[3];
	u16 rate_rssi;
	u16 rsv3[4];
	u8 destAdrs[6];
	u8 srcAdrs[6];
	u16 rsv4[4];
	u16 data[2];
} WMDcfRecvBuf, WMdcfRecvBuf;

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

typedef struct WMStatus {
	u16 state;
	u16 BusyApiid;
	BOOL apiBusy;
	BOOL scan_continue;
	BOOL mp_flag;
	BOOL dcf_flag;
	BOOL ks_flag;
	BOOL dcf_sendFlag;
	BOOL VSyncFlag;
	u8 wlVersion[8 ];
	u16 macVersion;
	u16 rfVersion;
	u16 bbpVersion[4 / sizeof(u16)];
	u16 mp_parentSize;
	u16 mp_childSize;
	u16 mp_parentMaxSize;
	u16 mp_childMaxSize;
	u16 mp_sendSize;
	u16 mp_recvSize;
	u16 mp_maxSendSize;
	u16 mp_maxRecvSize;
	u16 mp_parentVCount;
	u16 mp_childVCount;
	u16 mp_parentInterval;
	u16 mp_childInterval;
	OSTick mp_parentIntervalTick;
	OSTick mp_childIntervalTick;
	u16 mp_minFreq;
	u16 mp_freq;
	u16 mp_maxFreq;
	u16 mp_vsyncOrderedFlag;
	u16 mp_vsyncFlag;
	s16 mp_count;
	s16 mp_limitCount;
	u16 mp_resumeFlag;
	u16 mp_prevPollBitmap;
	u16 mp_prevWmHeader;
	u16 mp_prevTxop;
	u16 mp_prevDataLength;
	u16 mp_recvBufSel;
	u16 mp_recvBufSize;
	WMMpRecvBuf * mp_recvBuf[2];
	u32 * mp_sendBuf;
	u16 mp_sendBufSize;
	u16 mp_ackTime;
	u16 mp_waitAckFlag;
	u16 mp_readyBitmap;
	u16 mp_newFrameFlag;
	u16 mp_setDataFlag;
	u16 mp_sentDataFlag;
	u16 mp_bufferEmptyFlag;
	u16 mp_isPolledFlag;
	u16 mp_minPollBmpMode;
	u16 mp_singlePacketMode;
	u8 reserved_c[2];
	u16 mp_defaultRetryCount;
	u16 mp_ignoreFatalErrorMode;
	u16 mp_ignoreSizePrecheckMode;
	u16 mp_pingFlag;
	u16 mp_pingCounter;
	u8 dcf_destAdr[6 ];
	u16 * dcf_sendData;
	u16 dcf_sendSize;
	u16 dcf_recvBufSel;
	WMDcfRecvBuf * dcf_recvBuf[2];
	u16 dcf_recvBufSize;
	u16 curr_tgid;
	u16 linkLevel;
	u16 minRssi;
	u16 rssiCounter;
	u16 beaconIndicateFlag;
	u16 wepKeyId;
	u16 pwrMgtMode;
	u32 miscFlags;
	u16 VSyncBitmap;
	u16 valarm_queuedFlag;
	u32 v_tsf;
	u32 v_tsf_bak;
	u32 v_remain;
	u16 valarm_counter;
	u8 reserved_e[2];
	u8 MacAddress[6 ];
	u16 mode;
	WMParentParam pparam;
	u8 childMacAddress[15 ][6 ];
	u16 child_bitmap;
	WMBssDesc * pInfoBuf;
	u16 aid;
	u8 parentMacAddress[6 ];
	u16 scan_channel;
	u8 reserved_f[4];
	u16 wepMode;
	BOOL wep_flag;
	u16 wepKey[80 / sizeof(u16)];
	u16 rate;
	u16 preamble;
	u16 tmptt;
	u16 retryLimit;
	u16 enableChannel;
	u16 allowedChannel;
	u16 portSeqNo[15 + 1][8 ];
	WMPortSendQueueData sendQueueData[32 ];
	WMPortSendQueue sendQueueFreeList;
	WMPortSendQueue sendQueue[4 ];
	WMPortSendQueue readyQueue[4 ];
	OSMutex sendQueueMutex;
	BOOL sendQueueInUse;
	OSTick mp_lastRecvTick[1 + 15 ];
	OSTick mp_lifeTimeTick;
	u16 mp_current_minFreq;
	u16 mp_current_freq;
	u16 mp_current_maxFreq;
	u16 mp_current_minPollBmpMode;
	u16 mp_current_singlePacketMode;
	u16 mp_current_defaultRetryCount;
	u16 mp_current_ignoreFatalErrorMode;
	u8 reserved[2];
} WMStatus, WMstatus;

typedef struct WMArm7Buf {
	WMStatus * status;
	u8 reserved_a[4];
	u32 * fifo7to9;
	u8 reserved_b[4];
	WMBssDesc connectPInfo;
	u32 requestBuf[512 / sizeof(u32)];
} WMArm7Buf, WMarm7Buf;

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				buf[2];
} WlCmdReq;

typedef struct WMSPWork {
    OSMessageQueue toWLmsgQ;
    OSMessage toWLmsg[2 ];
    OSMessageQueue fromWLmsgQ;
    OSMessage fromWLmsg[4 ];
    OSMessageQueue confirmQ;
    OSMessage confirm[4 ];
    OSMessageQueue requestQ;
    OSMessage request[32 ];
    u32 requestStack[4096 / sizeof(u32)];
    u32 indicateStack[1024 / sizeof(u32)];
    OSMutex fifoExclusive;
    u32 dmaNo;
    OSArenaId arenaId;
    OSHeapHandle heapHandle;
    WMArm7Buf *wm7buf;
    WMStatus *status;
    u8 rssiHistory[32 ];
    u32 rssiIndex;
    u32 indPrio_high;
    u32 wlPrio_high;
    u32 reqPrio_high;
    u32 indPrio_low;
    u32 wlPrio_low;
    u32 reqPrio_low;
} WMSPWork;

extern WMSPWork native_utility_child_arm7_data_027f84f0;

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_utility_child_arm7_data_027f84f0;
}
