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

typedef struct NativeSequenceCacheView {
    u32 reserved00;
    const u8 *begin;
    const u8 *end;
    u8 bytes[16];
} NativeSequenceCacheView;
extern NativeSequenceCacheView native_host_arm7_data_03807ec0;
extern void native_host_arm7_arm_03800784(const u8 *);
u8 native_arm7_wram_03800290(NativeTrackInitializerView *track) {
    const u8 *address;
    u8 value;
    address = track->current;
    if ((u32)address < (u32)native_host_arm7_data_03807ec0.begin || (u32)address >= (u32)native_host_arm7_data_03807ec0.end) {
        native_host_arm7_arm_03800784(address);
    }
    value = native_host_arm7_data_03807ec0.bytes[(u32)address - (u32)native_host_arm7_data_03807ec0.begin];
    track->current++;
    return value;
}
