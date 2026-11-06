typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed long s32;
    typedef signed long long int s64;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef volatile u64 vu64;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
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
u16 native_fn_02007b3c(void);
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
typedef struct NVRAMConfigDate {
	u8 month;
	u8 day;
} NVRAMConfigDate;
typedef struct NVRAMConfigNickname {
	u16 str[10 ];
	u8 length;
	u8 rsv;
} NVRAMConfigNickname;
typedef struct NVRAMConfigComment {
	u16 str[26 ];
	u8 length;
	u8 rsv;
} NVRAMConfigComment;
typedef struct NVRAMConfigOwnerInfo {
	u8 favoriteColor :4;
	u8 rsv :4;
	NVRAMConfigDate birthday;
	u8 pad;
	NVRAMConfigNickname nickname;
	NVRAMConfigComment comment;
} NVRAMConfigOwnerInfo;
typedef struct NVRAMConfigAlarm {
	u8 hour;
	u8 minute;
	u8 second;
	u8 pad;
	u16 enableWeek :7;
	u16 alarmOn :1;
	u16 rsv :8;
} NVRAMConfigAlarm;
typedef struct NVRAMConfigTpCalibData {
	u16 raw_x1;
	u16 raw_y1;
	u8 dx1;
	u8 dy1;
	u16 raw_x2;
	u16 raw_y2;
	u8 dx2;
	u8 dy2;
} NVRAMConfigTpCalibData;
typedef struct NVRAMConfigOption {
	u16 language :3;
	u16 agbLcd :1;
	u16 detectPullOutCardFlag :1;
	u16 detectPullOutCtrdgFlag :1;
	u16 autoBootFlag :1;
	u16 rsv :4;
	u16 input_favoriteColor :1;
	u16 input_tp :1;
	u16 input_language :1;
	u16 input_rtc :1;
	u16 input_nickname :1;
	u8 timezone;
	u8 rtcClockAdjust;
	s64 rtcOffset;
} NVRAMConfigOption;
typedef struct NVRAMConfigData {
	u8 version;
	u8 pad;
	NVRAMConfigOwnerInfo owner;
	NVRAMConfigAlarm alarm;
	NVRAMConfigTpCalibData tp;
	NVRAMConfigOption option;
} NVRAMConfigData;
typedef struct NVRAMConfig {
	NVRAMConfigData ncd;
	u16 saveCount;
	u16 crc16;
} NVRAMConfig;
void native_main_02008360(u32 buffer[32 / sizeof(u32)]);
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
static s32 GX_GetVCount(void);
static inline s32 GX_GetVCount ()
{
	return (*( REGType16v *) (0x04000000 + 0x006)) ;
}
extern vu64 native_data_main_020e36fc;
void native_main_02008360 (u32 buffer[32 / sizeof(u32)])
{
    const OSSystemWork * work = ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ;
    const u8 * macAddress = (u8 *)((u32)(work->nvramUserInfo) + ((sizeof(NVRAMConfig) + 3) & ~0x00000003));
    buffer[0] = (u32)((GX_GetVCount() << 16) | native_fn_02007b3c());
    buffer[1] = (u32)(*(u16 *)(macAddress + 4) << 16) ^ (u32)(native_data_main_020e36fc);
    buffer[2] = (u32)(native_data_main_020e36fc >> 32) ^ *(u32 *)macAddress ^ work->vblankCount;
    buffer[2] ^= (*( REGType32v *) (0x04000000 + 0x600)) ;
    buffer[3] = *(u32 *)(&work->real_time_clock[0]);
    buffer[4] = *(u32 *)(&work->real_time_clock[4]);
    buffer[5] = (((u32)work->mic_sampling_data) << 16) ^ work->mic_last_address;
    buffer[6] = (u32)((*(u16 *)(&work->touch_panel[0]) << 16) | *(u16 *)(&work->touch_panel[2]));
    buffer[7] = (u32)((work->wm_rssi_pool << 16) | ((*(const REGType16v *) (0x04000000 + 0x130)) | *(vu16 *)(0x02000000 + 0x007fffa8) ));
}
