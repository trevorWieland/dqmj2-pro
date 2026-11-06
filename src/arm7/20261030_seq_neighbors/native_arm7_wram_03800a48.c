typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

typedef struct NativeModulation {
    u16 words[3];
} NativeModulation;

typedef struct NativeChannel NativeChannel;

struct NativeChannel {
    u8 reserved00[2];
    u8 envStatus;
    u8 reserved03;
    u8 panRange;
    u8 reserved05;
    s16 userFader;
    u8 reserved08[3];
    s8 userPan;
    s16 userVolume;
    s16 userPitch;
    u8 reserved10[18];
    u8 priority;
    u8 reserved23[5];
    NativeModulation modulation;
    u8 reserved2E[6];
    s32 length;
    u8 reserved38[24];
    NativeChannel *next;
};

typedef struct NativeTrack {
    u8 reserved00;
    u8 panRange;
    u8 reserved02[2];
    u8 volume;
    u8 expression;
    s8 pitchBend;
    u8 bendRange;
    s8 pan;
    s8 extPan;
    s16 extFader;
    s16 extPitch;
    u8 reserved0E[10];
    NativeModulation modulation;
    u8 reserved1E[30];
    NativeChannel *head;
} NativeTrack;

typedef struct NativePlayer {
    u32 reserved00;
    u8 reserved04;
    u8 volume;
    s16 extFader;
} NativePlayer;

typedef char NativeTrackSize[(sizeof(NativeTrack) == 0x40) ? 1 : -1];
typedef char NativeChannelSize[(sizeof(NativeChannel) == 0x54) ? 1 : -1];
typedef char NativePlayerSize[(sizeof(NativePlayer) == 8) ? 1 : -1];

extern void native_host_arm7_arm_037ffb1c(NativeChannel *);
void native_arm7_wram_03800a48(NativeTrack *track) {
    NativeChannel *channel;
    for (channel = track->head; channel; channel = channel->next) native_host_arm7_arm_037ffb1c(channel);
    track->head = 0;
}
