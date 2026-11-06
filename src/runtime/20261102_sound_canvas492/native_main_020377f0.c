typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed long s32;
        typedef int BOOL;
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
BOOL native_fn_02006eb8(OSMessageQueue * mq, OSMessage * msg, s32 flags);
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
    BOOL native_fn_020097b8(u32 flags);
    void native_fn_02009974(u32 tag);
    u32 native_fn_020099e0(void);
typedef enum SNDChannelOut {
	SND_CHANNEL_OUT_MIXER,
	SND_CHANNEL_OUT_BYPASS
} SNDChannelOut;
typedef enum SNDOutput {
	SND_OUTPUT_MIXER,
	SND_OUTPUT_CHANNEL1,
	SND_OUTPUT_CHANNEL3,
	SND_OUTPUT_CHANNEL1_3
} SNDOutput;
void native_fn_02009200(u32 chBitMask, u32 capBitMask, u32 alarmBitMask, u32 flags);
void native_fn_020093d8(
    SNDOutput left,
    SNDOutput right,
    SNDChannelOut channel1,
    SNDChannelOut channel3
);
typedef enum {
    NNS_SND_CAPTURE_FORMAT_PCM16,
    NNS_SND_CAPTURE_FORMAT_PCM8
} NNSSndCaptureFormat;
typedef enum {
    NNS_SND_CAPTURE_TYPE_REVERB,
    NNS_SND_CAPTURE_TYPE_EFFECT,
    NNS_SND_CAPTURE_TYPE_SAMPLING
} NNSSndCaptureType;
typedef void (*NNSSndCaptureCallback)(void * bufferL, void * bufferR, u32 len, NNSSndCaptureFormat format, void * arg);
void native_main_020377f0(void);
void native_fn_02038924(u32 chBitFlag);
void native_fn_02038954(u32 capBitFlag);
void native_fn_020389b8(int alarmNo);
typedef struct NNSSndFader {
    int origin;
    int target;
    int counter;
    int frame;
} NNSSndFader;
typedef struct CaptureParam {
    BOOL activeFlag;
    NNSSndCaptureType type;
    NNSSndCaptureFormat format;
    void * bufferL;
    void * bufferR;
    u32 bufLen;
    u32 blockSize;
    int curBuffer;
    u32 chBitMask;
    u32 playChBitMask;
    u32 capBitMask;
    int alarmNo;
    int interval;
    NNSSndCaptureCallback callback;
    void * callbackArg;
    NNSSndFader fader;
    BOOL fadeOutFlag;
    int volume;
} CaptureParam;
extern CaptureParam native_data_main_020f1f10;
extern OSMessageQueue native_data_main_020f1ed0;
void native_main_020377f0 (void)
{
    CaptureParam * cap = &native_data_main_020f1f10;
    u32 commandTag;
    BOOL useAlarm;
    if (!cap->activeFlag) return;
    useAlarm = cap->alarmNo >= 0 ? 1 : 0 ;
    native_fn_02009200(
        cap->playChBitMask,
        cap->capBitMask,
        useAlarm ? (u32)(1 << cap->alarmNo) : 0,
        0
        );
    if (useAlarm) {
        commandTag = native_fn_020099e0();
        (void)native_fn_020097b8((1 << 0) );
        native_fn_02009974(commandTag);
        while (native_fn_02006eb8(&native_data_main_020f1ed0, ((void *)0) , 0 )) {
        }
    }
    if (cap->capBitMask) native_fn_02038954(cap->capBitMask);
    if (cap->chBitMask) native_fn_02038924(cap->chBitMask);
    if (useAlarm) native_fn_020389b8(cap->alarmNo);
    if (cap->type == NNS_SND_CAPTURE_TYPE_EFFECT) {
        native_fn_020093d8(
            SND_OUTPUT_MIXER,
            SND_OUTPUT_MIXER,
            SND_CHANNEL_OUT_MIXER,
            SND_CHANNEL_OUT_MIXER
            );
    }
    cap->activeFlag = 0 ;
}
