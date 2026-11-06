typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef int BOOL;
#define TRUE 1
#define FALSE 0
#define NULL 0
#define SND_TRACK_MAX_CALL 3
#define SND_TRACK_COUNT_PER_PLAYER 16
#define SND_INST_PCM 1
#define SND_INST_PSG 2
#define SND_INST_NOISE 3
#define SND_INST_DIRECTPCM 4

enum SNDSeqVal { SND_SEQ_VAL_U8, SND_SEQ_VAL_U16, SND_SEQ_VAL_VLV, SND_SEQ_VAL_RAN, SND_SEQ_VAL_VAR };

typedef struct SNDTrack SNDTrack;
typedef struct SNDPlayer SNDPlayer;
typedef struct SNDExChannel SNDExChannel;
typedef struct SNDInstData SNDInstData;
typedef struct SNDBankData SNDBankData;
typedef struct SNDModParam SNDModParam;

struct SNDBankData;
struct SNDInstData { u8 type, reserved01; u16 wave, archive; u8 root, attack, decay, sustain, release, pan; };
struct SNDModParam { u8 target, speed, depth, range; u16 delay; };
struct SNDTrack;
struct SNDExChannel;
typedef void (*SNDExChannelCallback)(SNDExChannel *, int, void *);

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
    u8 priority, reserved23;
    u16 volume, reserved26;
    SNDModParam modulation;
    u16 delayCounter, phase;
    s16 sweepPitch;
    s32 length;
    u8 waveParameters[12];
    void *waveData;
    SNDExChannelCallback callback;
    void *callbackUserData;
    SNDExChannel *channelLLNext;
};

struct SNDTrack {
    struct { u8 active:1, noteWait:1, muted:1, tie:1, noteFinishWait:1, portamento:1, cmp:1, channelMask:1; } flags;
    u8 panRange;
    u16 program;
    u8 volume, expression;
    s8 pitchBend;
    u8 bendRange;
    s8 pan, extPan;
    s16 extFader, extPitch;
    u8 envAttack, envDecay, envSustain, envRelease, priority;
    s8 transpose;
    u8 portamentoKey, portamentoTime;
    s16 sweepPitch;
    SNDModParam mod;
    u16 channelMask;
    s32 wait;
    const u8 *base, *cur, *posCallStack[3];
    u8 loopCount[3], callStackDepth;
    SNDExChannel *channelLLHead;
};

struct SNDPlayer {
    struct { u8 active:1, prepared:1, paused:1, reserved:5; } flags;
    u8 playerId, reserved02[2], prio, volume;
    s16 extFader;
    u8 tracks[16];
    u16 tempo, tempoRatio, tempoCounter, reserved1E;
    SNDBankData *bank;
};

typedef char TrackSize[(sizeof(SNDTrack) == 64) ? 1 : -1];
typedef char ChannelSize[(sizeof(SNDExChannel) == 84) ? 1 : -1];
typedef char PlayerSize[(sizeof(SNDPlayer) == 36) ? 1 : -1];

extern SNDTrack *native_host_arm7_arm_03800a7c(SNDPlayer *, int);
extern void native_host_arm7_arm_03800784(const u8 *);
extern u8 native_host_arm7_arm_03800290(SNDTrack *);
extern int native_host_arm7_arm_038007f0(SNDTrack *, SNDPlayer *, int);
extern u32 native_host_arm7_arm_038007c0(SNDTrack *);
extern void native_host_arm7_arm_038009e0(SNDTrack *, SNDPlayer *, int);
extern void native_host_arm7_arm_03800a48(SNDTrack *);
extern void native_host_arm7_arm_038009d0(SNDTrack *, const u8 *, u32);
extern void native_host_arm7_arm_038018c8(SNDTrack *, SNDPlayer *, int);
extern s16 *native_host_arm7_arm_03801840(const SNDPlayer *, int);
extern u32 native_host_arm7_arm_037feec4(void);
extern void native_host_arm7_arm_03800aa8(SNDPlayer *, int);
extern BOOL native_host_arm7_arm_03801948(SNDBankData *, int, int, SNDInstData *);
extern SNDExChannel *native_host_arm7_arm_037ff950(u32, int, u32, SNDExChannelCallback, void *);
extern void native_host_arm7_arm_03800b38(SNDExChannel *, int, void *);
extern BOOL native_host_arm7_arm_03801b08(SNDExChannel *, int, int, int, SNDBankData *, const SNDInstData *);
extern void native_host_arm7_arm_037ffb1c(SNDExChannel *);
extern void native_host_arm7_arm_037ff8d4(SNDExChannel *, int);
extern void native_host_arm7_arm_037ff8f4(SNDExChannel *, int);
extern void native_host_arm7_arm_037ff910(SNDExChannel *, int);
extern void native_host_arm7_arm_037ff918(SNDExChannel *, int);
extern int native_host_arm7_data_03807ec0;
