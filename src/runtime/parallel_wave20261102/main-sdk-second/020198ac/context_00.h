typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed long s32;
typedef u32 OSIntrMode;
extern OSIntrMode native_fn_02007ff4(void);
extern OSIntrMode native_fn_02008008(OSIntrMode state);
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
void native_fn_020066ec(void);
void native_fn_020068d4(OSThreadQueue * queue);
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
void native_fn_02008d78(void * dest, u8 data, u32 size);
struct CTRDGTaskInfo_tag;
typedef u32 (*CTRDG_TASK_FUNC) (struct CTRDGTaskInfo_tag *);
typedef struct CTRDGTaskInfo_tag {
	CTRDG_TASK_FUNC task;
	CTRDG_TASK_FUNC callback;
	u32 result;
	u8 * data;
	u8 * adr;
	u32 offset;
	u32 size;
	u8 * dst;
	u16 sec_num;
	u8 busy;
	u8 param[1];
} CTRDGTaskInfo;
typedef struct {
	OSThread th[1];
	CTRDGTaskInfo * volatile list;
	CTRDGTaskInfo end_task;
} CTRDGiTaskWork;
extern const u16 (*ctrdgi_fl_maxtime);
void native_main_020198ac(void *arg);
typedef struct {
CTRDGiTaskWork *field_0000;
CTRDGTaskInfo field_0004;
u64 field_0028[1024 / sizeof(u64)];
} NativeStorage_020ec588;
extern NativeStorage_020ec588 native_data_main_020ec588;
static inline void MI_CpuClear8 (void * dest, u32 size)
{
	native_fn_02008d78(dest, 0, size);
}
