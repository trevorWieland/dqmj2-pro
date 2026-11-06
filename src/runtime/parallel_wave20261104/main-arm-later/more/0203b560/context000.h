typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef int BOOL;

typedef void (*PMSleepCallback) (void *);

typedef struct PMiSleepCallbackInfo PMSleepCallbackInfo;

struct PMiSleepCallbackInfo {
	PMSleepCallback callback;
	void * arg;
	PMSleepCallbackInfo * next;
};

static inline void PM_SetSleepCallbackInfo (PMSleepCallbackInfo * info, PMSleepCallback callback, void * arg)
{
	info->callback = callback;
	info->arg = arg;
}

typedef struct {
    void * prevObject;
    void * nextObject;
} NNSFndLink;

typedef struct {
    void * headObject;
    void * tailObject;
    u16 numObjects;
    u16 offset;
} NNSFndList;

void native_fn_0202b9dc(NNSFndList * list, u16 offset);

typedef enum NNSSndStrmFormat {
    NNS_SND_STRM_FORMAT_PCM8,
    NNS_SND_STRM_FORMAT_PCM16
} NNSSndStrmFormat;

typedef enum NNSSndStrmCallbackStatus {
    NNS_SND_STRM_CALLBACK_SETUP,
    NNS_SND_STRM_CALLBACK_INTERVAL
} NNSSndStrmCallbackStatus;

typedef void (*NNSSndStrmCallback)(NNSSndStrmCallbackStatus status, int numChannles, void * buffer[], u32 len, NNSSndStrmFormat format, void * arg);

typedef struct NNSSndStrm {
    NNSFndLink link;
    PMSleepCallbackInfo preSleepInfo;
    PMSleepCallbackInfo postSleepInfo;
    NNSSndStrmFormat format;
    BOOL activeFlag :1;
    BOOL startFlag :1;
    u32 chBufLen;
    int interval;
    NNSSndStrmCallback callback;
    void * callbackArg;
    int curBuffer;
    int volume;
    int alarmNo;
    u32 chBitMask;
    int numChannels;
    u8 channelNo[16 ];
} NNSSndStrm;

void native_main_0203b560(NNSSndStrm * stream);

extern NNSFndList native_data_020f5b00;

static void native_fn_0203ba70(void * arg);

static void native_fn_0203babc(void * arg);

extern BOOL native_data_020f5afc;
