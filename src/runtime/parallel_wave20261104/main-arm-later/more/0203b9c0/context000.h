typedef unsigned char u8;

typedef unsigned long u32;

typedef int BOOL;

typedef void (*PMSleepCallback) (void *);

typedef struct PMiSleepCallbackInfo PMSleepCallbackInfo;

struct PMiSleepCallbackInfo {
	PMSleepCallback callback;
	void * arg;
	PMSleepCallbackInfo * next;
};

typedef struct {
    void * prevObject;
    void * nextObject;
} NNSFndLink;

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

typedef struct NNSSndStrmChannel {
    void * buffer;
    int volume;
} NNSSndStrmChannel;

extern NNSSndStrmChannel native_data_020f5b4c[16];

void native_main_0203b9c0(NNSSndStrm * stream, NNSSndStrmCallbackStatus status);

extern void *native_data_020f5b0c[16];
