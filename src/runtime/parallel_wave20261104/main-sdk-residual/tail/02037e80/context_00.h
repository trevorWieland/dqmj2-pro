typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed char s8;
typedef signed short int s16;
typedef signed long s32;
typedef int BOOL;
typedef struct OSiAlarm OSAlarm;
typedef u64 OSTick;
typedef void (*OSAlarmHandler) (void *);
struct OSiAlarm {
	OSAlarmHandler handler;
	void * arg;
	u32 tag;
	OSTick fire;
	OSAlarm * prev;
	OSAlarm * next;
	OSTick period;
	OSTick start;
};
void native_fn_020072d0(void * startAddr, u32 nBytes);
typedef struct SNDAlarm {
	u8 enable;
	u8 id;
	u16 padding;
	struct {
		OSTick tick;
		OSTick period;
	} setting;
	OSAlarm alarm;
} SNDAlarm;
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
typedef struct SNDCommand {
	struct SNDCommand * next;
	SNDCommandID id;
	u32 arg[4];
} SNDCommand;
const SNDCommand * native_fn_020095e8(u32 flags);
BOOL native_fn_020097b8(u32 flags);
u32 native_fn_020099e0(void);
BOOL native_fn_02009a0c(u32 tag);
typedef enum {
	SND_DUTY_1_8,
	SND_DUTY_2_8,
	SND_DUTY_3_8,
	SND_DUTY_4_8,
	SND_DUTY_5_8,
	SND_DUTY_6_8,
	SND_DUTY_7_8
} SNDDuty;
struct SNDExChannel;
typedef enum SNDExChannelCallbackStatus {
	SND_EX_CHANNEL_CALLBACK_DROP,
	SND_EX_CHANNEL_CALLBACK_FINISH
} SNDExChannelCallbackStatus;
typedef void (*SNDExChannelCallback) (struct SNDExChannel * ch_p, SNDExChannelCallbackStatus status, void * userData);
typedef struct SNDWaveParam {
        u8 format;
        u8 loopflag;
        u16 rate;
        u16 timer;
        u16 loopstart;
        u32 looplen;
    } SNDWaveParam;
typedef struct SNDLfoParam {
	u8 target;
	u8 speed;
	u8 depth;
	u8 range;
	u16 delay;
} SNDLfoParam;
typedef struct SNDLfo {
	struct SNDLfoParam param;
	u16 delay_counter;
	u16 counter;
} SNDLfo;
typedef struct SNDExChannel {
	u8 myNo;
	u8 type;
	u8 env_status;
	u8 active_flag : 1;
	u8 start_flag : 1;
	u8 auto_sweep : 1;
	u8 sync_flag : 5;
	u8 pan_range;
	u8 original_key;
	s16 user_decay2;
	u8 key;
	u8 velocity;
	s8 init_pan;
	s8 user_pan;
	s16 user_decay;
	s16 user_pitch;
	s32 env_decay;
	s32 sweep_counter;
	s32 sweep_length;
	u8 attack;
	u8 sustain;
	u16 decay;
	u16 release;
	u8 prio;
	u8 pan;
	u16 volume;
	u16 timer;
	struct SNDLfo lfo;
	s16 sweep_pitch;
	s32 length;
	struct SNDWaveParam wave;
	union {
		const void * data;
		SNDDuty duty;
	};
	SNDExChannelCallback callback;
	void * callback_data;
	struct SNDExChannel * nextLink;
} SNDExChannel;
struct SNDBankData;
typedef struct SNDPlayer {
	u8 active_flag :1;
	u8 prepared_flag :1;
	u8 pause_flag :1;
	u8 pad_ :5;
	u8 myNo;
	u8 pad2_;
	u8 pad3_;
	u8 prio;
	u8 volume;
	s16 extFader;
	u8 tracks[16 ];
	u16 tempo;
	u16 tempo_ratio;
	u16 tempo_counter;
	u16 pad__;
	struct SNDBankData * bank;
} SNDPlayer;
typedef struct SNDTrack {
	u8 active_flag :1;
	u8 note_wait :1;
	u8 mute_flag :1;
	u8 tie_flag :1;
	u8 note_finish_wait :1;
	u8 porta_flag :1;
	u8 cmp_flag :1;
	u8 channel_mask_flag :1;
	u8 pan_range;
	u16 prgNo;
	u8 volume;
	u8 volume2;
	s8 pitch_bend;
	u8 bend_range;
	s8 pan;
	s8 ext_pan;
	s16 extFader;
	s16 ext_pitch;
	u8 attack;
	u8 decay;
	u8 sustain;
	u8 release;
	u8 prio;
	s8 transpose;
	u8 porta_key;
	u8 porta_time;
	s16 sweep_pitch;
	struct SNDLfoParam mod;
	u16 channel_mask;
	s32 wait;
	const u8 * base;
	const u8 * cur;
	const u8 * call_stack[3 ];
	u8 loop_count[3 ];
	u8 call_stack_depth;
	struct SNDExChannel * channel_list;
} SNDTrack;
struct SNDBankData;
struct SNDDriverInfo;
void native_fn_02009400(struct SNDDriverInfo *info);
typedef struct SNDWork {
	SNDExChannel channel[16 ];
	SNDPlayer player[16 ];
	SNDTrack track[32 ];
	SNDAlarm alarm[8 ];
} SNDWork;
typedef struct SNDDriverInfo {
	SNDWork work;
	u32 chCtrl[16 ];
	SNDWork * workAddress;
	u32 lockedChannels;
	u32 padding[6];
} SNDDriverInfo;
typedef struct SNDBinaryFileHeader {
	char signature[4];
	u16 byteOrder;
	u16 version;
	u32 fileSize;
	u16 headerSize;
	u16 dataBlocks;
} SNDBinaryFileHeader;
typedef struct SNDBinaryBlockHeader {
	u32 kind;
	u32 size;
} SNDBinaryBlockHeader;
struct SNDWaveArc;
struct SNDExChannel;
typedef struct SNDWaveArcLink {
	struct SNDWaveArc * waveArc;
	struct SNDWaveArcLink * next;
} SNDWaveArcLink;
typedef struct SNDWaveArc {
	struct SNDBinaryFileHeader fileHeader;
	struct SNDBinaryBlockHeader blockHeader;
	struct SNDWaveArcLink * topLink;
	u32 reserved[7];
	u32 waveCount;
	u32 waveOffset[0];
} SNDWaveArc;
typedef struct SNDBankData {
	struct SNDBinaryFileHeader fileHeader;
	struct SNDBinaryBlockHeader blockHeader;
	struct SNDWaveArcLink waveArcLink[4 ];
	u32 instCount;
	u32 instOffset[0];
} SNDBankData;
struct SNDBankData;
BOOL native_main_02037e80(void);
typedef void (*PMSleepCallback) (void *);
typedef struct PMiSleepCallbackInfo PMSleepCallbackInfo;
struct PMiSleepCallbackInfo {
	PMSleepCallback callback;
	void * arg;
	PMSleepCallbackInfo * next;
};
struct SNDBankData;
typedef struct {
s8 field_0000;
unsigned char padding_0001[3];
BOOL field_0004;
u32 field_0008;
} NativeStorage_020f1f64;
extern NativeStorage_020f1f64 native_data_main_020f1f64;

extern __attribute__ ((aligned(32))) SNDDriverInfo native_data_main_020f1fa0[2];
