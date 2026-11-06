typedef unsigned long u32;
        typedef int BOOL;
    BOOL native_fn_020097b8(u32 flags);
    void native_fn_02009974(u32 tag);
    u32 native_fn_020099e0(void);
void native_fn_02009200(u32 chBitMask, u32 capBitMask, u32 alarmBitMask, u32 flags);
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
void native_main_020378d8(void);
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
void native_main_020378d8 (void)
{
    CaptureParam * cap;
    u32 commandTag;
    cap = &native_data_main_020f1f10;
    if (!cap->activeFlag) return;
    native_fn_02009200(
        cap->playChBitMask,
        cap->capBitMask,
        cap->alarmNo >= 0 ? (u32)(1 << cap->alarmNo) : 0,
        0
        );
    commandTag = native_fn_020099e0();
    (void)native_fn_020097b8((1 << 0) );
    native_fn_02009974(commandTag);
}
