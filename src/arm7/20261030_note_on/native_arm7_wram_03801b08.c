typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct NativeInstrument {
    u8 type;
    u8 reserved;
    u16 wave;
    u16 archive;
    u8 root;
    u8 attack;
    u8 decay;
    u8 sustain;
    u8 release;
    u8 pan;
} NativeInstrument;
typedef struct NativeWaveArchive { u8 prefix[0x38]; u32 count; } NativeWaveArchive;
typedef struct NativeWaveLink { const NativeWaveArchive *archive; u32 reserved; } NativeWaveLink;
typedef struct NativeBankView { u8 prefix[0x18]; NativeWaveLink links[4]; } NativeBankView;
typedef struct NativeChannelNoteView {
    u8 reserved00[5];
    u8 root;
    u8 reserved06[2];
    u8 midi;
    u8 velocity;
    s8 pan;
} NativeChannelNoteView;
extern const u8 *native_host_arm7_arm_03801ac8(const NativeWaveArchive *, int);
extern int native_host_arm7_arm_037ff760(NativeChannelNoteView *, const void *, const void *, int);
extern int native_host_arm7_arm_037ff79c(NativeChannelNoteView *, int, int);
extern int native_host_arm7_arm_037ff7e8(NativeChannelNoteView *, int);
extern void native_host_arm7_arm_037ff8d4(NativeChannelNoteView *, int);
extern void native_host_arm7_arm_037ff8f4(NativeChannelNoteView *, int);
extern void native_host_arm7_arm_037ff910(NativeChannelNoteView *, int);
extern void native_host_arm7_arm_037ff918(NativeChannelNoteView *, int);
int native_arm7_wram_03801b08(NativeChannelNoteView *channel, int midi, int velocity, int length,
        const NativeBankView *bank, const NativeInstrument *instrument) {
    const NativeWaveArchive *archive;
    const u8 *wave;
    int release = instrument->release;
    int result;
    int archive_index;
    int wave_index;
    if (release == 255) {
        length = -1;
        release = 0;
    }
    switch (instrument->type) {
        case 1:
        case 4:
            if (instrument->type == 1) {
                archive_index = instrument->archive;
                wave_index = instrument->wave;
                archive = bank->links[archive_index].archive;
                if (!archive)
                    wave = 0;
                else if ((u32)wave_index >= archive->count)
                    wave = 0;
                else
                    wave = native_host_arm7_arm_03801ac8(archive, wave_index);
            } else {
                wave = (const u8 *)(((u32)instrument->archive << 16) | (u32)instrument->wave);
            }
            if (!wave)
                result = 0;
            else
                result = native_host_arm7_arm_037ff760(channel, wave, wave + 12, length);
            break;
        case 2:
            result = native_host_arm7_arm_037ff79c(channel, instrument->wave, length);
            break;
        case 3:
            result = native_host_arm7_arm_037ff7e8(channel, length);
            break;
        default:
            result = 0;
            break;
    }
    if (!result)
        return 0;
    channel->midi = (u8)midi;
    channel->root = instrument->root;
    channel->velocity = (u8)velocity;
    native_host_arm7_arm_037ff8d4(channel, instrument->attack);
    native_host_arm7_arm_037ff8f4(channel, instrument->decay);
    native_host_arm7_arm_037ff910(channel, instrument->sustain);
    native_host_arm7_arm_037ff918(channel, release);
    channel->pan = (s8)(instrument->pan - 64);
    return 1;
}
