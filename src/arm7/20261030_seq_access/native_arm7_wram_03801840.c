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

typedef struct NativePlayerIdView { u8 flags; u8 id; } NativePlayerIdView;
extern u8 *native_host_arm7_data_03807edc;
s16 *native_arm7_wram_03801840(NativePlayerIdView *player, int index) {
    u8 *work;
    work = native_host_arm7_data_03807edc;
    if (work == 0) return 0;
    if (index < 16) return (s16 *)((u32)work + 0x20u + (u32)player->id * 0x24u + (u32)index * 2u);
    return (s16 *)((u32)work + 0x260u + (u32)(index - 16) * 2u);
}
