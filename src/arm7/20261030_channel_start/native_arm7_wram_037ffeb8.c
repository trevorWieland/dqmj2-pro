typedef unsigned char u8;
typedef unsigned short u16;
typedef struct NativeChannelStartFlags { u8 active : 1; u8 start : 1; u8 reserved : 6; } NativeChannelStartFlags;
typedef struct NativeChannelStartView {
    u8 reserved00[2];
    u8 envelopeStatus;
    NativeChannelStartFlags flags;
    u8 reserved04[12];
    int attenuation;
    u8 reserved14[26];
    u16 lfoDelayCounter;
    u16 lfoCounter;
    u16 reserved32;
    int length;
} NativeChannelStartView;
typedef char StartViewSize[(sizeof(NativeChannelStartView) == 56) ? 1 : -1];
void native_arm7_wram_037ffeb8(NativeChannelStartView *channel, int length) {
    channel->attenuation = -92544;
    channel->envelopeStatus = 0;
    channel->length = length;
    channel->lfoCounter = 0;
    channel->lfoDelayCounter = 0;
    channel->flags.start = 1;
    channel->flags.active = 1;
}
