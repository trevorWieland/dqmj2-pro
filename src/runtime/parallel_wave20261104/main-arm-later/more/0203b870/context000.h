typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef int BOOL;

typedef enum {
	SND_CHANNEL_DATASHIFT_NONE,
	SND_CHANNEL_DATASHIFT_1BIT,
	SND_CHANNEL_DATASHIFT_2BIT,
	SND_CHANNEL_DATASHIFT_4BIT
} SNDChannelDataShift;

void native_fn_020092e4(u32 chBitMask, int volume, SNDChannelDataShift shift);

u16 native_fn_02009e60(int dB);

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

void native_main_0203b870(NNSSndStrm * stream, int volume);

typedef struct NNSSndStrmChannel {
    void * buffer;
    int volume;
} NNSSndStrmChannel;

extern NNSSndStrmChannel native_data_020f5b4c[16];
