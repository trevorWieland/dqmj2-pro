typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef volatile s16 vs16;
typedef int BOOL;
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
void native_main_02009514(void);
struct SNDCommand * native_fn_020096f8(u32 flags);
void native_fn_02009780(struct SNDCommand * command);
BOOL native_fn_020097b8(u32 flags);
typedef struct SNDSharedWork {
	vu32 finishCommandTag;
	vu32 playerStatus;
	vu16 channelStatus;
	vu16 captureStatus;
	vu32 padding[5];
	struct {
		vs16 variable[16 ];
		vu32 tickCounter;
	} player[16 ];
	vs16 globalVariable[16 ];
} SNDSharedWork;
extern SNDSharedWork * native_data_main_020e52c0;
void native_fn_02009de4(SNDSharedWork * work);
typedef struct {
SNDCommand * field_0000;
u32 field_0004;
SNDCommand * field_0008;
SNDCommand * field_000c;
SNDCommand * field_0010;
int field_0014;
int field_0018;
int field_001c;
u32 field_0020;
SNDCommand * field_0024[8 + 1];
unsigned char padding_0048[24];
__attribute__ ((aligned(32))) SNDSharedWork field_0060;
__attribute__ ((aligned(32))) SNDCommand field_02e0[256 ];
} NativeStorage_020e3780;
extern NativeStorage_020e3780 native_data_main_020e3780;
void native_fn_02009b14(void);
SNDCommand * native_fn_020096f8 (u32 flags);
void native_fn_02009780 (struct SNDCommand * command);
BOOL native_fn_020097b8 (u32 flags);
void native_fn_02009b14 (void);
