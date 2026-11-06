typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef volatile u32 vu32;
        typedef int BOOL;
extern u32 native_data_main_027e0000[];
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
        typedef u32 OSIrqMask;
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
void native_fn_020068d4(OSThreadQueue * queue);
static inline void OS_ClearIrqCheckFlag (OSIrqMask intr)
{
	*(vu32 *)((((u32)native_data_main_027e0000) + 0x00003fc0) + 0x38) &= (u32) ~intr;
}
static inline OSIrqMask OS_GetIrqCheckFlag (void)
{
	return *(OSIrqMask *)((((u32)native_data_main_027e0000) + 0x00003fc0) + 0x38) ;
}
void native_main_020059b8(BOOL clear, OSIrqMask irqFlags);
    OSThreadQueue native_data_main_027e0060 = { ((void *)0) , ((void *)0) };
void native_main_020059b8 (BOOL clear, OSIrqMask irqFlags)
{
    OSIntrMode enabled = native_fn_02007ff4();
    if (clear) {
        (void)OS_ClearIrqCheckFlag(irqFlags);
    }
    (void)native_fn_02008008(enabled);
    while (!(OS_GetIrqCheckFlag() & irqFlags)) {
        native_fn_020068d4(&native_data_main_027e0060);
    }
}
