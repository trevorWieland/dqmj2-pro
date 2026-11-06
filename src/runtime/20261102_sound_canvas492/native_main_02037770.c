typedef unsigned long u32;
        typedef int BOOL;
typedef enum {
	SND_CHANNEL_DATASHIFT_NONE,
	SND_CHANNEL_DATASHIFT_1BIT,
	SND_CHANNEL_DATASHIFT_2BIT,
	SND_CHANNEL_DATASHIFT_4BIT
} SNDChannelDataShift;
void native_fn_020092e4(u32 chBitMask, int volume, SNDChannelDataShift shift);
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
void native_main_02037770(void);
void native_fn_020377f0(void);
typedef struct NNSSndFader {
    int origin;
    int target;
    int counter;
    int frame;
} NNSSndFader;
int native_fn_020379ec(const NNSSndFader * fader);
void native_fn_02037a20(NNSSndFader * fader);
BOOL native_fn_02037a38(const NNSSndFader * fader);
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
void native_main_02037770 (void)
{
    CaptureParam * cap;
    NNSSndFader * fader;
    int volume;
    cap = &native_data_main_020f1f10;
    if (cap->activeFlag && cap->type == NNS_SND_CAPTURE_TYPE_REVERB) {
        fader = &cap->fader;
        native_fn_02037a20(fader);
        if (cap->fadeOutFlag) {
            if (native_fn_02037a38(fader)) {
                native_fn_020377f0();
                return;
            }
        }
        volume = (native_fn_020379ec(fader) >> 8);
        if (volume != cap->volume) {
            native_fn_020092e4(
                cap->playChBitMask,
                volume,
                SND_CHANNEL_DATASHIFT_NONE
                );
            cap->volume = volume;
        }
    }
}
void native_fn_020377f0 (void);
