typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;

typedef struct NativeTrackFlags {
    u8 active : 1;
    u8 noteWait : 1;
    u8 muted : 1;
    u8 tie : 1;
    u8 noteFinishWait : 1;
    u8 portamento : 1;
    u8 compare : 1;
    u8 channelMask : 1;
} NativeTrackFlags;

typedef struct NativeModulation {
    u16 words[3];
} NativeModulation;

typedef struct NativeTrackInitializerView {
    NativeTrackFlags flags;
    u8 panRange;
    u16 program;
    u8 volume;
    u8 expression;
    s8 pitchBend;
    u8 bendRange;
    s8 pan;
    s8 extPan;
    s16 extFader;
    s16 extPitch;
    u8 envAttack;
    u8 envDecay;
    u8 envSustain;
    u8 envRelease;
    u8 priority;
    s8 transpose;
    u8 portamentoKey;
    u8 portamentoTime;
    s16 sweepPitch;
    NativeModulation modulation;
    u16 channelMask;
    int wait;
    const u8 *base;
    const u8 *current;
    u8 reserved2C[15];
    u8 callStackDepth;
    void *head;
} NativeTrackInitializerView;

typedef char TrackViewSize[(sizeof(NativeTrackInitializerView) == 64) ? 1 : -1];

extern void native_host_arm7_arm_037ffd90(NativeModulation *);

void native_arm7_wram_038008f0(NativeTrackInitializerView *track) {
    track->base = 0;
    track->current = 0;
    track->flags.noteWait = 1;
    track->flags.muted = 0;
    track->flags.tie = 0;
    track->flags.noteFinishWait = 0;
    track->flags.portamento = 0;
    track->flags.compare = 1;
    track->flags.channelMask = 0;
    track->callStackDepth = 0;
    track->program = 0;
    track->priority = 64;
    track->volume = 127;
    track->expression = 127;
    track->extFader = 0;
    track->pan = 0;
    track->extPan = 0;
    track->pitchBend = 0;
    track->extPitch = 0;
    track->envAttack = 255;
    track->envDecay = 255;
    track->envSustain = 255;
    track->envRelease = 255;
    track->panRange = 127;
    track->bendRange = 2;
    track->portamentoKey = 60;
    track->portamentoTime = 0;
    track->sweepPitch = 0;
    track->transpose = 0;
    track->channelMask = 0xFFFF;
    native_host_arm7_arm_037ffd90(&track->modulation);
    track->wait = 0;
    track->head = 0;
}
