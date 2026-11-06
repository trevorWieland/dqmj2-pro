typedef unsigned long u32;
typedef enum {
	SND_WAVE_FORMAT_PCM8,
	SND_WAVE_FORMAT_PCM16,
	SND_WAVE_FORMAT_ADPCM,
	SND_WAVE_FORMAT_PSG,
	SND_WAVE_FORMAT_NOISE = SND_WAVE_FORMAT_PSG
} SNDWaveFormat;
typedef enum {
	SND_CHANNEL_LOOP_MANUAL,
	SND_CHANNEL_LOOP_REPEAT,
	SND_CHANNEL_LOOP_1SHOT
} SNDChannelLoop;
typedef enum {
	SND_CHANNEL_DATASHIFT_NONE,
	SND_CHANNEL_DATASHIFT_1BIT,
	SND_CHANNEL_DATASHIFT_2BIT,
	SND_CHANNEL_DATASHIFT_4BIT
} SNDChannelDataShift;
void native_main_0200932c(
    int chNo,
    SNDWaveFormat format,
    const void *dataAddr,
    SNDChannelLoop loop,
    int loopStart,
    int dataLen,
    int volume,
    SNDChannelDataShift shift,
    int timer,
    int pan
);
typedef enum SNDCommandID {
	SND_COMMAND_START_SEQ,
	SND_COMMAND_STOP_SEQ,
	SND_COMMAND_PREPARE_SEQ,
	SND_COMMAND_START_PREPARED_SEQ,
	SND_COMMAND_PAUSE_SEQ,
	SND_COMMAND_SKIP_SEQ,
	SND_COMMAND_PLAYER_PARAM,
	SND_COMMAND_TRACK_PARAM,
	SND_COMMAND_MUTE_TRACK,
	SND_COMMAND_ALLOCATABLE_CHANNEL,
	SND_COMMAND_PLAYER_LOCAL_VAR,
	SND_COMMAND_PLAYER_GLOBAL_VAR,
	SND_COMMAND_START_TIMER,
	SND_COMMAND_STOP_TIMER,
	SND_COMMAND_SETUP_CHANNEL_PCM,
	SND_COMMAND_SETUP_CHANNEL_PSG,
	SND_COMMAND_SETUP_CHANNEL_NOISE,
	SND_COMMAND_SETUP_CAPTURE,
	SND_COMMAND_SETUP_ALARM,
	SND_COMMAND_CHANNEL_TIMER,
	SND_COMMAND_CHANNEL_VOLUME,
	SND_COMMAND_CHANNEL_PAN,
	SND_COMMAND_SURROUND_DECAY,
	SND_COMMAND_MASTER_VOLUME,
	SND_COMMAND_MASTER_PAN,
	SND_COMMAND_OUTPUT_SELECTOR,
	SND_COMMAND_LOCK_CHANNEL,
	SND_COMMAND_UNLOCK_CHANNEL,
	SND_COMMAND_STOP_UNLOCKED_CHANNEL,
	SND_COMMAND_SHARED_WORK,
	SND_COMMAND_INVALIDATE_SEQ,
	SND_COMMAND_INVALIDATE_BANK,
	SND_COMMAND_INVALIDATE_WAVE,
	SND_COMMAND_READ_DRIVER_INFO
} SNDCommandID;
extern void native_fn_02009470(SNDCommandID command, u32 arg0, u32 arg1, u32 arg2, u32 arg3);
void native_main_0200932c (int chNo,
                          SNDWaveFormat format,
                          const void * dataaddr,
                          SNDChannelLoop loop,
                          int loopStart,
                          int loopLen, int volume, SNDChannelDataShift shift, int timer, int pan)
{
    native_fn_02009470((SND_COMMAND_SETUP_CHANNEL_PCM), (u32)( timer << 16 | chNo), (u32)( dataaddr), (u32)( volume << 24 | shift << 22 | loopLen), (u32)( loop << 26 | format << 24 | pan << 16 | loopStart))
                ;
}
void native_fn_02009470 (SNDCommandID id, u32 arg0, u32 arg1, u32 arg2, u32 arg3);
