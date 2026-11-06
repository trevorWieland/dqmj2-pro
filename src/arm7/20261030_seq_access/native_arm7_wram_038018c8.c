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

extern void native_host_arm7_arm_038009e0(NativeTrackInitializerView *, void *, int);
extern void native_host_arm7_arm_03800a48(NativeTrackInitializerView *);
void native_arm7_wram_038018c8(NativeTrackInitializerView *track, void *player, int mode) {
    switch (mode) {
        case 0:
            track->flags.muted = 0;
            break;
        case 1:
            track->flags.muted = 1;
            break;
        case 2:
            track->flags.muted = 1;
            native_host_arm7_arm_038009e0(track, player, -1);
            break;
        case 3:
            track->flags.muted = 1;
            native_host_arm7_arm_038009e0(track, player, 127);
            native_host_arm7_arm_03800a48(track);
            break;
    }
}
