typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef unsigned long long int u64;

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

typedef struct OSThreadInfo {
    u16 isNeedRescheduling;
    u16 irqDepth;
    OSThread * current;
    OSThread * list;
    void * switchCallback;
} OSThreadInfo;

typedef volatile struct OSLockWord {
	u32 lockFlag;
	u16 ownerID;
	u16 extension;
} OSLockWord;

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

BOOL native_host_arm7_arm_037fc760(OSMessageQueue * mq, OSMessage * msg, s32 flags);

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

typedef struct {
	u8 bootCheckInfo[0x20];
	u32 resetParameter;
	u8 padding5[0x8];
	u32 romBaseOffset;
	u8 cartridgeModuleInfo[12];
	u32 vblankCount;
	u8 wmBootBuf[0x40];
	u8 nvramUserInfo[0x100];
	u8 isd_reserved1[0x20];
	u8 arenaInfo[0x48];
	u8 real_time_clock[8];
	u32 dmaClearBuf[4];
	u8 rom_header[0x160];
	u8 isd_reserved2[32];
	u32 pxiSignalParam[2];
	u32 pxiHandleChecker[2];
	u32 mic_last_address;
	u16 mic_sampling_data;
	u16 wm_callback_control;
	u16 wm_rssi_pool;
	u8 ctrdg_SetModuleInfoFlag;
	u8 ctrdg_IsExisting;
	u32 component_param;
	OSThreadInfo * threadinfo_mainp;
	OSThreadInfo * threadinfo_subp;
	u16 button_XY;
	u8 touch_panel[4];
	u16 autoloadSync;
	u32 lockIDFlag_mainp[2];
	u32 lockIDFlag_subp[2];
	struct OSLockWord lock_VRAM_C;
	struct OSLockWord lock_VRAM_D;
	struct OSLockWord lock_WRAM_BLOCK0;
	struct OSLockWord lock_WRAM_BLOCK1;
	struct OSLockWord lock_CARD;
	struct OSLockWord lock_CARTRIDGE;
	struct OSLockWord lock_INIT;
	u16 mmem_checker_mainp;
	u16 mmem_checker_subp;
	u8 padding4[2];
	u16 command_area;
} OSSystemWork;

typedef struct RTCRawDate {
	u32 year :8;
	u32 month :5;
	u32 dummy0 :3;
	u32 day :6;
	u32 dummy1 :2;
	u32 week :3;
	u32 dummy2 :5;
} RTCRawDate;

typedef struct RTCRawTime {
	u32 hour :6;
	u32 afternoon :1;
	u32 dummy0 :1;
	u32 minute :7;
	u32 dummy1 :1;
	u32 second :7;
	u32 dummy2 :9;
} RTCRawTime;

typedef struct RTCRawStatus1 {
	u16 reset :1;
	u16 format :1;
	u16 dummy0 :2;
	u16 intr1 :1;
	u16 intr2 :1;
	u16 bld :1;
	u16 poc :1;
	u16 dummy1 :8;
} RTCRawStatus1;

typedef struct RTCRawStatus2 {
	u16 intr_mode :4;
	u16 dummy0 :2;
	u16 intr2_mode :1;
	u16 test :1;
	u16 dummy1 :8;
} RTCRawStatus2;

typedef struct RTCRawAlarm {
	u32 week :3;
	u32 dummy0 :4;
	u32 we :1;
	u32 hour :6;
	u32 afternoon :1;
	u32 he :1;
	u32 minute :7;
	u32 me :1;
	u32 dummy2 :8;
} RTCRawAlarm;

typedef struct RTCRawPulse {
	u32 pulse :5;
	u32 dummy :27;
} RTCRawPulse;

typedef struct RTCRawAdjust {
	u32 adjust :8;
	u32 dummy :24;
} RTCRawAdjust;

typedef struct RTCRawFree {
	u32 free :8;
	u32 dummy :24;
} RTCRawFree;

typedef union RTCRawData {
	struct {
		RTCRawDate date;
		RTCRawTime time;
	} t;
	struct {
		RTCRawStatus1 status1;
		RTCRawStatus2 status2;
		union {
			RTCRawPulse pulse;
			RTCRawAlarm alarm;
			RTCRawAdjust adjust;
			RTCRawFree free;
		};
	} a;
	u32 words[2];
	u16 halfs[4];
	u8 bytes[8];
} RTCRawData;

typedef enum RTCPxiResult {
	RTC_PXI_RESULT_SUCCESS = 0,
	RTC_PXI_RESULT_INVALID_COMMAND,
	RTC_PXI_RESULT_ILLEGAL_STATUS,
	RTC_PXI_RESULT_BUSY,
	RTC_PXI_RESULT_FATAL_ERROR,
	RTC_PXI_RESULT_MAX
} RTCPxiResult;

typedef struct RTCWork {
    OSMessageQueue msgQueue;
    OSMessage msgArray[4 ];
    OSThread thread;
    u64 stack[256 / sizeof(u64)];
    BOOL busy;
    u16 command;
    OSThread polling;
    OSThreadQueue pollingQueue;
    u64 pollingStack[256 / sizeof(u64)];
    OSAlarm pollingAlarm;
} RTCWork;

void native_host_arm7_arm_027f6638(void);

void native_host_arm7_arm_027f667c(u16 format);

void native_host_arm7_arm_027f67a0(RTCRawData *data);

void native_host_arm7_arm_027f67cc(const RTCRawData *data);

void native_host_arm7_arm_027f6804(RTCRawDate *date);

void native_host_arm7_arm_027f6830(RTCRawTime *time);

void native_host_arm7_arm_027f685c(const RTCRawTime *time);

BOOL native_host_arm7_arm_027f6894(RTCRawPulse *pulse);

BOOL native_host_arm7_arm_027f68fc(const RTCRawPulse *pulse);

BOOL native_host_arm7_arm_027f6970(RTCRawAlarm *alarm);

BOOL native_host_arm7_arm_027f69d4(const RTCRawAlarm *alarm);

BOOL native_host_arm7_arm_027f6a44(RTCRawAlarm *alarm);

BOOL native_host_arm7_arm_027f6aa4(const RTCRawAlarm *alarm);

void native_host_arm7_arm_027f6b10(RTCRawStatus1 *stat);

void native_host_arm7_arm_027f6b3c(const RTCRawStatus1 *stat);

void native_host_arm7_arm_027f6b74(RTCRawStatus2 *stat);

void native_host_arm7_arm_027f6ba0(const RTCRawStatus2 *stat);

void native_host_arm7_arm_027f6bd8(RTCRawAdjust *adjust);

void native_host_arm7_arm_027f6c04(const RTCRawAdjust *adjust);

void native_host_arm7_arm_027f6c3c(RTCRawFree *free);

void native_host_arm7_arm_027f6c68(const RTCRawFree *free);

extern const u16 (*ctrdgi_fl_maxtime);

typedef struct {u8 opaquePrefix[4];RTCWork work;} RTCImportedView;

extern RTCImportedView native_host_arm7_data_027f8e34;

extern void native_host_arm7_arm_027f6074(u16 command, RTCPxiResult result);

void native_host_arm7_main_027f60b4(void *arg);

void native_host_arm7_arm_027f6074(u16 command, RTCPxiResult result);
