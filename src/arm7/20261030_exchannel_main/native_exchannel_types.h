typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef signed long long s64;
typedef int BOOL;
#define TRUE 1
#define FALSE 0
#define SND_CHANNEL_COUNT 16
#define SND_CHN_TYPE_PSG 1
#define SND_ENV_RELEASE 3
#define SND_CHN_SYNC_START 1
#define SND_CHN_SYNC_STOP 2
#define SND_CHN_SYNC_TIMER 4
#define SND_CHN_SYNC_VOLUME 8
#define SND_CHN_SYNC_PAN 16
#define SND_LFO_PITCH 0
#define SND_LFO_VOLUME 1
#define SND_LFO_PAN 2
struct SNDLfoParam { u8 target, speed, depth, range; u16 delay; };
struct SNDLfo { struct SNDLfoParam param; u16 delayCounter, phase; };
struct SNDWaveParam { u8 format, loopEnabled; u16 reserved02, timer, reserved06; u32 loopLength; };
struct SNDExChannel;
typedef void (*SNDExChannelCallback)(struct SNDExChannel *, int, void *);
struct SNDExChannel {
    u8 id, type, envStatus;
    struct { u8 active:1, start:1, autoSweep:1, syncFlag:5; } flags;
    u8 panRange, rootMidiKey;
    s16 userDecay2;
    u8 midiKey, velocity;
    s8 initPan, userPan;
    s16 userDecay, userPitch;
    s32 envAttenuation, sweepCounter, sweepLength;
    u8 attack, sustain;
    u16 decay, release;
    u8 priority, pan;
    u16 volume, timer;
    struct SNDLfo lfo;
    s16 sweepPitch;
    s32 length;
    struct SNDWaveParam waveParam;
    void *waveDataPtr;
    SNDExChannelCallback callback;
    void *callbackUserData;
    struct SNDExChannel *channelLLNext;
};
typedef char ChannelSize[(sizeof(struct SNDExChannel) == 84) ? 1 : -1];
extern struct SNDExChannel native_host_arm7_data_03807ee0[16];
extern const s16 native_host_arm7_data_0380704c[];
extern BOOL native_host_arm7_arm_037feb50(int);
extern int native_host_arm7_arm_037ff82c(struct SNDExChannel *, BOOL);
extern int native_host_arm7_arm_037ffe14(const struct SNDLfo *);
extern void native_host_arm7_arm_037ffdb4(struct SNDLfo *);
extern u16 native_host_arm7_arm_037fedd8(int);
extern u16 native_host_arm7_arm_037fecac(int, int);
