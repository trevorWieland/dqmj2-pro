typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef unsigned long long int u64;

typedef signed long s32;

typedef volatile u16 vu16;

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

typedef	struct {
	u16			length;
	u8			rate;
	u8			rssi;
	u16			aid;
	u16			noResponse;
	u8			cdata[4];
} WlMpKeyData;

typedef	struct {
	u16			bitmap;
	u16			errBitmap;
	u16			count;
	u16			length;
	u16			txCount;
	WlMpKeyData	data[1];
} WlMpKey;

typedef	struct {
	struct {
		u32		success;
		u32		failed;
		u32		retry;
		u32		ackErr;
		u32		unicast;
		u32		multicast;
		u32		wep;
		u32		beacon;
	} tx;
	struct {
		u32		rts;
		u32		fragment;
		u32		unicast;
		u32		multicast;
		u32		wep;
		u32		beacon;
		u32		fcsErr;
		u32		duplicateErr;
		u32		mpDuplicateErr;
		u32		icvErr;
		u32		fcErr;
		u32		lengthErr;
		u32		plcpErr;
		u32		bufOvfErr;
		u32		pathErr;
		u32		rateErr;
		u32		fcsOk;
	} rx;
	struct {
		u32		txMp;
		u32		txKey;
		u32		txNull;
		u32		rxMp;
		u32		rxMpAck;
		u32		keyResponseErr[15];
	} multiPoll;
} WlCounter;

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	u16		length;
	u16		rssi;
	u16		bssid[3];
	u16		ssidLength;
	u8		ssid[32];
	u16		capaInfo;
	struct {
		u16	basic;
		u16	support;
	} rateSet;
	u16		beaconPeriod;
	u16		dtimPeriod;
	u16		channel;
	u16		cfpPeriod;
	u16		cfpMaxDuration;
	u16		gameInfoLength;
	u16		otherElementCount;
	union _element {
		u8		gameInfo[4];
		u8		otherElement[4];
	};
} WlBssDesc;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				mib;
} WlMlmeResetReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmeResetCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				pwrMgtMode;
	u16				wakeUp;
	u16				recieveDtims;
} WlMlmePowerMgtReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmePowerMgtCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				bssid[3];
	u16				ssidLength;
	u8				ssid[32];
	u16				scanType;
	u8				channelList[16];
	u16				maxChannelTime;
	u16				bssidMaskCount;
	u16				bssidMask[3];
} WlMlmeScanReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				foundMap;
	u16				bssDescCount;
	WlBssDesc		bssDescList[1];
} WlMlmeScanCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				timeOut;
	u16				rsv;
	WlBssDesc		bssDesc;
} WlMlmeJoinReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				statusCode;
	u16				peerMacAdrs[3];
} WlMlmeJoinCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				algorithm;
	u16				timeOut;
} WlMlmeAuthReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				statusCode;
	u16				peerMacAdrs[3];
	u16				algorithm;
} WlMlmeAuthCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				reasonCode;
} WlMlmeDeAuthReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				peerMacAdrs[3];
} WlMlmeDeAuthCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				listenInterval;
	u16				timeOut;
} WlMlmeAssReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				statusCode;
	u16				aid;
} WlMlmeAssCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				newApMacAdrs[3];
	u16				listenInterval;
	u16				timeOut;
} WlMlmeReAssReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				statusCode;
	u16				aid;
} WlMlmeReAssCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				peerMacAdrs[3];
	u16				reasonCode;
} WlMlmeDisAssReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmeDisAssCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				ssidLength;
	u8				ssid[32];
	u16				beaconPeriod;
	u16				dtimPeriod;
	u16				channel;
	u16				basicRateSet;
	u16				supportRateSet;
	u16				gameInfoLength;
	u8				gameInfo[2];
} WlMlmeStartReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmeStartCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				rsv;
	u16				ccaMode;
	u16				edThreshold;
	u16				measureTime;
	u8				channelList[16];
} WlMlmeMeasChanReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				reserved;
	u16				ccaBusyInfo[16];
} WlMlmeMeasChanCfm;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	WlMpKey			mpKey;
} WlMaMpEndInd;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				buf[2];
} WlCmdCfm;

typedef struct {
	u16			state;
	u16			aid;
	u16			macAdrs[3];
	u16			rssi;
	u16			capaInfo;
	u16			authSeed;
	u16			supRateSet;
	u16			rsv;
	u16			lastSeqCtrl;
	u16			frameCount;
	u16			lifeTime;
	u16			maxLifeTime;
} WlStaElement;

typedef	struct {
	u16	rssi;
	u16	channel;
	u16	capaInfo;
	u16	bssid[3];
	u16	ssidLength;
	u8	ssid[32];
	u16	beaconInterval;
	u16	lifeTime;
} WlApElement;

extern const u16 (*ctrdgi_fl_maxtime);

typedef struct {
    u16 NextId;
    u16 Flag;
    void (*pTaskFunc)(void);
} TASK_TBL, *LPTASK_TBL;

typedef struct {
    u16 EnQ[4 ];
    u16 DeQ[4 ];
    vu16 NextPri;
    u16 TaskPri;
    u16 CurrTaskID;
    u16 pad;
    OSThread Thread;
    TASK_TBL TaskTbl[24 ];
} TASK_MAN, *LPTASK_MAN;
