typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef volatile u16 vu16;
typedef volatile u64 vu64;
typedef u16 REGType16;
typedef int BOOL;
typedef u32 OSIntrMode;
typedef u64 OSTick;
#define NULL ((void *)0)
#define TRUE 1
#define FALSE 0
#define OS_PROCMODE_IRQ 0x12
#define OS_THREAD_LAUNCHER_PRIORITY 16
#define OS_THREAD_SPECIFIC_MAX 3
#define HW_PSR_DISABLE_IRQ 0x80
#define HW_WRAM 0x037f8000
#define HW_PRV_WRAM_IRQ_STACK_END 0x0380ff80
#define OS_MESSAGE_BLOCK 1
#define OS_TIMER_0 0
#define reg_OS_TM0CNT_L (*(volatile u16 *)0x04000100)
#define reg_OS_IF (*(volatile u32 *)0x04000214)
#define OS_MilliSecondsToTicks(value) (((u64)(value)*33514)/64)
typedef struct OSContext { u32 cpsr,r[13],sp,lr,pc_plus4,sp_svc; } OSContext;
typedef struct OSThread OSThread;
typedef struct OSMutex OSMutex;
typedef struct { OSThread *head,*tail; } OSThreadQueue;
typedef struct { OSThread *prev,*next; } OSThreadLink;
typedef struct { OSMutex *head,*tail; } OSMutexQueue;
typedef struct { OSMutex *next,*prev; } OSMutexLink;
typedef void (*OSSwitchThreadCallback)(OSThread *,OSThread *);
typedef void (*OSThreadDestructor)(void *);
typedef enum { OS_THREAD_STATE_WAITING=0,OS_THREAD_STATE_READY=1,OS_THREAD_STATE_TERMINATED=2 } OSThreadState;
typedef struct OSAlarm { u8 opaque[44]; } OSAlarm;
struct OSThread { OSContext context; OSThreadState state; OSThread *next; u32 id,priority; void *profiler;
    OSThreadQueue *queue; OSThreadLink link; OSMutex *mutex; OSMutexQueue mutexQueue;
    u32 stackTop,stackBottom,stackWarningOffset; OSThreadQueue joinQueue; void *specific[3];
    OSAlarm *alarmForSleep; OSThreadDestructor destructor; void *userParameter; u32 systemErrno; };
struct OSMutex { OSThreadQueue queue; OSThread *thread; s32 count; OSMutexLink link; };
typedef struct OSThreadInfo { u16 isNeedRescheduling,irqDepth; OSThread *current,*list; void *switchCallback; } OSThreadInfo;
typedef void *OSMessage;
typedef struct { OSThreadQueue queueSend,queueReceive; OSMessage *msgArray; s32 msgCount,firstIndex,usedCount; } OSMessageQueue;
struct NativeThreadGlobals { u32 unknown0; u32 rescheduleCount; OSThread **currentThreadPtr; BOOL initialized;
    void *systemCallback; u8 pad14[8]; void *destructorStack; s32 threadIdCount; OSThreadInfo info; };
struct NativeTickGlobals { u16 useTick,padding; BOOL needResetTimer; OSTick counter; };
struct NativeSystemWork { u8 prefix[0x3a4]; OSThreadInfo *threadinfo_subp; };
typedef char ThreadSize[(sizeof(OSThread)==0xa4)?1:-1];
typedef char ContextSize[(sizeof(OSContext)==0x48)?1:-1];
typedef char MutexSize[(sizeof(OSMutex)==24)?1:-1];
typedef char QueueSize[(sizeof(OSMessageQueue)==32)?1:-1];
typedef char GlobalsSize[(sizeof(struct NativeThreadGlobals)==0x34)?1:-1];
struct NativeThreadSystem { struct NativeThreadGlobals state; OSThread idle,launcher; };
extern struct NativeThreadSystem native_host_arm7_data_038076f0;
extern struct NativeTickGlobals native_host_arm7_data_03807898;
extern OSThread native_host_arm7_data_03807724;
extern OSThread native_host_arm7_data_038077c8;
extern OSThreadInfo native_host_arm7_data_03807714;
extern char SDK_SYS_STACKSIZE[];
extern char SDK_IRQ_STACKSIZE[];
#define OSi_ThreadInfo native_host_arm7_data_038076f0.state.info
#define OSi_ThreadIdCount native_host_arm7_data_038076f0.state.threadIdCount
#define OSi_RescheduleCount native_host_arm7_data_038076f0.state.rescheduleCount
#define OSi_IsThreadInitialized native_host_arm7_data_038076f0.state.initialized
#define OSi_CurrentThreadPtr native_host_arm7_data_038076f0.state.currentThreadPtr
#define OSi_SystemCallbackInSwitchThread native_host_arm7_data_038076f0.state.systemCallback
#define OSi_StackForDestructor native_host_arm7_data_038076f0.state.destructorStack
#define OSi_LauncherThread native_host_arm7_data_038076f0.launcher
#define OSi_IdleThread native_host_arm7_data_038076f0.idle
#define OSi_TickCounter native_host_arm7_data_03807898.counter
#define OSi_GetCurrentThread() (*OSi_CurrentThreadPtr)
#define OS_SetCurrentThread(thread) (OSi_ThreadInfo.current=(thread))
#define OS_IsThreadRunnable(thread) ((thread)->state==OS_THREAD_STATE_READY)
#define OS_GetSystemWork() ((struct NativeSystemWork *)0x027ffc00)
static inline void OS_InitThreadQueue(OSThreadQueue *queue) { queue->head=queue->tail=NULL; }
static inline void OS_SetThreadDestructor(OSThread *thread,OSThreadDestructor destructor) { thread->destructor=destructor; }
extern u32 native_host_arm7_arm_037fdd00(void);
extern u32 native_host_arm7_arm_037fdd14(u32);
extern u32 native_host_arm7_arm_037fdd58(void);
extern BOOL native_host_arm7_arm_037fc64c(OSContext *);
extern void native_host_arm7_arm_037fc680(OSContext *);
extern void native_host_arm7_arm_037fc5c8(OSContext *,u32,u32);
extern void native_host_arm7_arm_037fdfd0(u32,void *,u32);
extern void native_host_arm7_arm_037fd3a0(OSAlarm *);
extern void native_host_arm7_arm_037fd4dc(OSAlarm *,OSTick,void (*)(void *),void *);
extern void native_host_arm7_arm_037fc50c(void *);
extern void native_host_arm7_arm_037fc15c(void);
extern void native_host_arm7_arm_037fc220(void);
extern void native_host_arm7_arm_037fc290(OSThreadQueue *);
extern void native_host_arm7_arm_037fc36c(OSThread *);
extern void native_host_arm7_arm_037fde70(void);
extern OSMutex *native_host_arm7_arm_037fbdbc(OSMutexQueue *);
#define OS_DisableInterrupts native_host_arm7_arm_037fdd00
#define OS_RestoreInterrupts native_host_arm7_arm_037fdd14
#define OS_GetProcMode native_host_arm7_arm_037fdd58
#define OS_SaveContext native_host_arm7_arm_037fc64c
#define OS_LoadContext native_host_arm7_arm_037fc680
#define OS_InitContext native_host_arm7_arm_037fc5c8
#define MI_CpuClear32(destination,size) native_host_arm7_arm_037fdfd0(0,(destination),(size))
#define OS_CreateAlarm native_host_arm7_arm_037fd3a0
#define OS_SetAlarm native_host_arm7_arm_037fd4dc
#define OSi_SleepAlarmCallback native_host_arm7_arm_037fc50c
#define OS_ExitThread native_host_arm7_arm_037fc15c
#define OSi_ExitThread_Destroy native_host_arm7_arm_037fc220
#define OS_SleepThread native_host_arm7_arm_037fc290
#define OS_WakeupThreadDirect native_host_arm7_arm_037fc36c
#define OS_Terminate native_host_arm7_arm_037fde70
#define OSi_RemoveMutexLinkFromQueue native_host_arm7_arm_037fbdbc
#define OS_GetCurrentThread() (OSi_ThreadInfo.current)
extern void native_host_arm7_arm_037fbcec(OSThreadQueue *,OSThread *);
#define OSi_InsertLinkToQueue native_host_arm7_arm_037fbcec
extern OSThread * native_host_arm7_arm_037fbd64(OSThreadQueue *,OSThread *);
#define OSi_RemoveSpecifiedLinkFromQueue native_host_arm7_arm_037fbd64
extern void native_host_arm7_arm_037fbdec(OSThread *);
#define OSi_InsertThreadToList native_host_arm7_arm_037fbdec
extern void native_host_arm7_arm_037fbe4c(OSThread *);
#define OSi_RemoveThreadFromList native_host_arm7_arm_037fbe4c
extern void native_host_arm7_arm_037fbe90(void);
#define OSi_RescheduleThread native_host_arm7_arm_037fbe90
extern void native_host_arm7_arm_037fbf64(void);
#define OS_InitThread native_host_arm7_arm_037fbf64
extern void native_host_arm7_arm_037fc054(OSThread *,void (*)(void *),void *,void *,u32,u32);
#define OS_CreateThread native_host_arm7_arm_037fc054
extern void native_host_arm7_arm_037fc180(OSThread *,void *);
#define OSi_ExitThread_ArgSpecified native_host_arm7_arm_037fc180
extern void native_host_arm7_arm_037fc1e0(void *);
#define OSi_ExitThread native_host_arm7_arm_037fc1e0
extern void native_host_arm7_arm_037fc2e4(OSThreadQueue *);
#define OS_WakeupThread native_host_arm7_arm_037fc2e4
extern OSThread * native_host_arm7_arm_037fc398(void);
#define OS_SelectThread native_host_arm7_arm_037fc398
extern BOOL native_host_arm7_arm_037fc3c0(OSThread *,u32);
#define OS_SetThreadPriority native_host_arm7_arm_037fc3c0
extern void native_host_arm7_arm_037fc468(u32);
#define OS_Sleep native_host_arm7_arm_037fc468
extern u32 native_host_arm7_arm_037fc558(void);
#define OS_DisableScheduler native_host_arm7_arm_037fc558
extern BOOL native_host_arm7_arm_037fc6d4(OSMessageQueue *,OSMessage,s32);
#define OS_SendMessage native_host_arm7_arm_037fc6d4
extern BOOL native_host_arm7_arm_037fc760(OSMessageQueue *,OSMessage *,s32);
#define OS_ReceiveMessage native_host_arm7_arm_037fc760
extern BOOL native_host_arm7_arm_037fc7fc(OSMessageQueue *,OSMessage *,s32);
#define OS_ReadMessage native_host_arm7_arm_037fc7fc
extern void native_host_arm7_arm_037fc90c(OSMutex *);
#define OS_UnlockMutex native_host_arm7_arm_037fc90c
extern void native_host_arm7_arm_037fc96c(OSThread *);
#define OSi_UnlockAllMutex native_host_arm7_arm_037fc96c
extern OSTick native_host_arm7_arm_037fd21c(void);
#define OS_GetTick native_host_arm7_arm_037fd21c
static inline s32 OSi_GetUnusedThreadId(void) { return ++OSi_ThreadIdCount; }
static inline OSThread *OSi_RemoveLinkFromQueue(OSThreadQueue *queue)
{
    OSThread *thread=queue->head;
    if (thread) {
        OSThread *next=thread->link.next;
        queue->head=next;
        if (next) next->link.prev=NULL;
        else { queue->tail=NULL; thread->queue=NULL; }
    }
    return thread;
}

extern OSSwitchThreadCallback OS_SetSwitchThreadCallback(OSSwitchThreadCallback);
