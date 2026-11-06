typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed long s32;
        typedef int BOOL;
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
BOOL native_fn_02006acc(OSThread * thread, u32 prio);
u32 native_fn_02006b74(const OSThread * thread);
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
extern const u16 (*ctrdgi_fl_maxtime);
struct MBiTaskInfo_tag;
typedef void (*MB_TASK_FUNC) (struct MBiTaskInfo_tag *);
typedef struct MBiTaskInfo_tag {
	struct MBiTaskInfo_tag * next;
	u32 busy : 1;
	u32 priority : 31;
	MB_TASK_FUNC task;
	MB_TASK_FUNC callback;
	u32 param[4];
} MBiTaskInfo;
typedef struct {
	OSThread th[1];
	MBiTaskInfo * volatile list;
	MBiTaskInfo end_task;
} MBiTaskWork;
void native_main_02018afc (void * arg)
{
	MBiTaskWork * const p = (MBiTaskWork *) arg;
	for (;;) {
		MBiTaskInfo * trg = ((void *)0) ;
		{
			OSIntrMode bak_cpsr = native_fn_02007ff4();
			while (!p->list) {
				(void)native_fn_02006acc(p->th, 0 );
				native_fn_020068d4(((void *)0) );
			}
			trg = p->list;
			p->list = p->list->next;
			(void)native_fn_02006acc(p->th, trg->priority);
			(void)native_fn_02008008(bak_cpsr);
		}
		if (trg->task)
			(*trg->task)(trg);
		{
			OSIntrMode bak_cpsr = native_fn_02007ff4();
			MB_TASK_FUNC callback = trg->callback;
			const u32 cur_priority = native_fn_02006b74(p->th);
			u32 new_priority;
			if (!p->list)
				new_priority = 0 ;
			else if (cur_priority < p->list->priority)
				new_priority = p->list->priority;
			else
				new_priority = cur_priority;
			if (new_priority != cur_priority)
				(void)native_fn_02006acc(p->th, new_priority);
			trg->next = ((void *)0) ;
			trg->busy = 0 ;
			if (callback)
				(*callback)(trg);
			if (trg == &p->end_task)
				break;
			(void)native_fn_02008008(bak_cpsr);
		}
	}
	((void)0) ;
	native_fn_020066ec();
	return;
}
