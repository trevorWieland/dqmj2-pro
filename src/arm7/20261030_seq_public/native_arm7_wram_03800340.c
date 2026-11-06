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

typedef struct NativePlayerFlags {
    u8 active : 1;
    u8 prepared : 1;
    u8 paused : 1;
    u8 reserved : 5;
} NativePlayerFlags;
typedef struct NativePlayerView {
    NativePlayerFlags flags;
    u8 playerId;
    u8 reserved02[6];
    u8 tracks[16];
    u8 reserved18[12];
} NativePlayerView;
typedef struct NativeSharedStatus { u32 unknown; u32 status; } NativeSharedStatus;
typedef char PlayerViewSize[(sizeof(NativePlayerView) == 36) ? 1 : -1];
extern NativePlayerView native_host_arm7_data_03808420[];
extern NativeSharedStatus *native_host_arm7_data_03807edc;
extern NativeTrackInitializerView *native_host_arm7_arm_03800a7c(NativePlayerView *, int);
extern void native_host_arm7_arm_03800b00(NativePlayerView *);
extern void native_host_arm7_arm_038009e0(NativeTrackInitializerView *, NativePlayerView *, int);
extern void native_host_arm7_arm_03800a48(NativeTrackInitializerView *);
extern void native_host_arm7_arm_038018c8(NativeTrackInitializerView *, NativePlayerView *, int);
void native_arm7_wram_03800340(int player) {
    NativePlayerView *current = &native_host_arm7_data_03808420[player];
    if (current->flags.active) {
        native_host_arm7_arm_03800b00(current);
        if (native_host_arm7_data_03807edc)
            native_host_arm7_data_03807edc->status &= ~(1u << player);
    }
}
