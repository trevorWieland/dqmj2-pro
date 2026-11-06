typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed long s32;
typedef volatile u32 vu32;
typedef int BOOL;
extern u32 native_data_main_027e0000[];
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
typedef void (*OSSwitchThreadCallback) (OSThread * from, OSThread * to);
void native_main_02006498(void);
void native_fn_020065f0(OSThread * thread, void (*func)(void *), void * arg, void * stack, u32 stackSize, u32 prio);
OSSwitchThreadCallback native_fn_02006c38(OSSwitchThreadCallback callback);
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
extern void native_data_main_00001000(void);
extern void native_data_main_00001000(void);
extern void native_data_main_027e0080(void);
void native_fn_02006c60(void *);
void native_fn_020065f0 (OSThread * thread, void (*func)(void *), void * arg, void * stack, u32 stackSize, u32 prio);
typedef struct {
void * field_0000;
u32 field_0004;
OSThread ** field_0008;
BOOL field_000c;
u32 field_0010;
vu32 field_0014;
vu32 field_0018;
void * field_001c;
int field_0020;
OSThreadInfo field_0024;
OSThread field_0034;
OSThread field_00f4;
u32 field_01b4[((sizeof(u32) * 2 + 0x40) + (sizeof(u32) * 32)) / sizeof(u32)];
} NativeStorage_020e33c0;
extern NativeStorage_020e33c0 native_data_main_020e33c0;
OSSwitchThreadCallback native_fn_02006c38 (OSSwitchThreadCallback callback);
void native_fn_02006c60 (void *);
static inline OSThreadInfo * OS_GetThreadInfo (void)
{
    return &native_data_main_020e33c0.field_0024;
}
static inline void OS_InitThreadQueue (OSThreadQueue * queue)
{
    queue->head = queue->tail = ((void *)0) ;
}
static inline void OS_SetCurrentThread (OSThread * thread)
{
    OS_GetThreadInfo()->current = thread;
}
