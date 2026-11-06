typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef unsigned long long int u64;

typedef signed long s32;

typedef volatile u16 vu16;

typedef vu16 REGType16v;

typedef int BOOL;

typedef u32 OSIntrMode;

extern OSIntrMode native_host_arm7_arm_037fdd00(void);

extern OSIntrMode native_host_arm7_arm_037fdd14(OSIntrMode state);

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

typedef enum SPIDeviceType {
	SPI_DEVICE_TYPE_TP = 0,
	SPI_DEVICE_TYPE_NVRAM,
	SPI_DEVICE_TYPE_MIC,
	SPI_DEVICE_TYPE_PM,
	SPI_DEVICE_TYPE_ARM7,
	SPI_DEVICE_TYPE_MAX
} SPIDeviceType;

void native_host_arm7_arm_03803a48(u16 command, u16 result);

BOOL native_host_arm7_arm_03803b7c(SPIDeviceType type, u32 process, u16 args, ...);

typedef enum {
    MIC_STATUS_READY = 0,
    MIC_STATUS_AUTO_START,
    MIC_STATUS_AUTO_SAMPLING,
    MIC_STATUS_AUTO_END,
    MIC_STATUS_END_WAIT,
} MICStatus;

typedef struct MICWork {
    u16 command[16 ];
    MICStatus status;
    u16 type;
    u16 admode;
    void *buf;
    u32 index;
    u32 size;
    u16 timerValue;
    u16 timerPrescaler;
    u16 temp16;
    u16 temporary;
} MICWork;

void native_host_arm7_wram_03805418(u32 data);

extern const u16 (*ctrdgi_fl_maxtime);

extern MICWork native_host_arm7_data_0380b258;

extern u16 native_host_arm7_mic_words_0380b258[16];

extern BOOL native_host_arm7_arm_038056e0(u32 value);
