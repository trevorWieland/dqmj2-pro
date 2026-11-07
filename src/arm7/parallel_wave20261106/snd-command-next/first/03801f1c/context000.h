typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef unsigned long long int u64;

typedef signed char s8;

typedef signed short int s16;

typedef signed long s32;

typedef volatile u8 vu8;

typedef volatile u16 vu16;

typedef volatile u32 vu32;

typedef volatile s16 vs16;

typedef vu8 REGType8v;

typedef vu16 REGType16v;

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

void native_host_arm7_wram_03801f1c(void);

typedef u32 OSIntrMode;

extern OSIntrMode native_host_arm7_arm_037fdd00(void);

extern OSIntrMode native_host_arm7_arm_037fdd14(OSIntrMode state);

typedef struct OSContext {
	u32 cpsr;
	u32 r[13];
	u32 sp;
	u32 lr;
	u32 pc_plus4;
	u32 sp_svc;
} OSContext;

typedef struct _OSThread OSThread;

typedef struct _OSThreadQueue OSThreadQueue;

typedef struct _OSThreadLink OSThreadLink;

typedef struct _OSMutexQueue OSMutexQueue;

typedef struct _OSMutexLink OSMutexLink;

typedef struct OSMutex OSMutex;

typedef struct OSiAlarm OSAlarm;

struct _OSThreadQueue {
        OSThread * head;
        OSThread * tail;
    };

struct _OSThreadLink {
        OSThread * prev;
        OSThread * next;
    };

struct _OSMutexQueue {
        OSMutex * head;
        OSMutex * tail;
    };

struct _OSMutexLink {
        OSMutex * next;
        OSMutex * prev;
    };

typedef enum {
    OS_THREAD_STATE_WAITING       = 0,
    OS_THREAD_STATE_READY         = 1,
    OS_THREAD_STATE_TERMINATED    = 2
} OSThreadState;

typedef void (*OSThreadDestructor) (void *);

struct _OSThread {
    OSContext context;
    OSThreadState state;
    OSThread * next;
    u32 id;
    u32 priority;
    void * profiler;
    OSThreadQueue * queue;
    OSThreadLink link;
    OSMutex * mutex;
    OSMutexQueue mutexQueue;
    u32 stackTop;
    u32 stackBottom;
    u32 stackWarningOffset;
    OSThreadQueue joinQueue;
    void * specific[3 ];
    OSAlarm * alarmForSleep;
    OSThreadDestructor destructor;
    void * userParameter;
    int systemErrno;
};

typedef struct OSMessageQueue OSMessageQueue;

typedef void * OSMessage;

struct OSMessageQueue {
	OSThreadQueue queueSend;
	OSThreadQueue queueReceive;
	OSMessage * msgArray;
	s32 msgCount;
	s32 firstIndex;
	s32 usedCount;
};

BOOL native_host_arm7_arm_037fc760(OSMessageQueue * mq, OSMessage * msg, s32 flags);

struct OSMutex {
	OSThreadQueue queue;
	OSThread * thread;
	s32 count;
	OSMutexLink link;
};

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

void native_host_arm7_arm_037fdfec(const void * srcp, void * destp, u32 size);

static inline void MI_CpuCopy32 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_host_arm7_arm_037fdfec(src, dest, size);
}

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
	SND_DUTY_1_8,
	SND_DUTY_2_8,
	SND_DUTY_3_8,
	SND_DUTY_4_8,
	SND_DUTY_5_8,
	SND_DUTY_6_8,
	SND_DUTY_7_8
} SNDDuty;

typedef enum {
	SND_CHANNEL_DATASHIFT_NONE,
	SND_CHANNEL_DATASHIFT_1BIT,
	SND_CHANNEL_DATASHIFT_2BIT,
	SND_CHANNEL_DATASHIFT_4BIT
} SNDChannelDataShift;

static inline void SND_StartChannel (int chNo)
        {
            ((void) 0) ;
            *((REGType8v *)((0x04000000 + 0x403) + ((chNo) << 4) ))
                |= 0x80 ;
        }

void native_host_arm7_arm_037fe804(int chNo,
                            const void * dataaddr,
                            SNDWaveFormat format,
                            SNDChannelLoop loop,
                            int loopStart,
                            int loopLen, int volume, SNDChannelDataShift shift, int timer, int pan);

void native_host_arm7_arm_037fe8d0(int chNo,
                            SNDDuty duty,
                            int volume, SNDChannelDataShift shift, int timer, int pan);

void native_host_arm7_arm_037fe97c(int chNo, int volume, SNDChannelDataShift shift, int timer, int pan);

void native_host_arm7_arm_037fea20(int chNo, s32 flags);

void native_host_arm7_arm_037fea48(int chNo, int volume, SNDChannelDataShift shift);

void native_host_arm7_arm_037feac0(int chNo, int timer);

void native_host_arm7_arm_037fead8(int chNo, int pan);

void native_host_arm7_arm_037feb6c(int pan);

u32 native_host_arm7_arm_037febd0(int chNo);

void native_host_arm7_arm_037febe0(int decay);

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

void native_host_arm7_arm_037ffd14(const void * start, const void * end);

void native_host_arm7_arm_037ffbe0(u32 chBitMask, u32 flags);

void native_host_arm7_arm_037ffcc0(u32 chBitMask, u32 flags);

void native_host_arm7_arm_037ffb30(u32 chBitMask, u32 flags);

u32 native_host_arm7_arm_037ffcf8(u32 flags);

typedef enum {
	SND_SEQ_MUTE_OFF,
	SND_SEQ_MUTE_NO_STOP,
	SND_SEQ_MUTE_RELEASE,
	SND_SEQ_MUTE_STOP
} SNDSeqMute;

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

void native_host_arm7_arm_03800310(int playerNo, const void * seqBase, u32 seqOffset, struct SNDBankData * bank_p);

void native_host_arm7_arm_03800340(int playerNo);

void native_host_arm7_arm_038000b4(int playerNo, const void * seqBase, u32 seqOffset, struct SNDBankData * bank_p);

void native_host_arm7_arm_038002f0(int playerNo);

void native_host_arm7_arm_0380039c(int playerNo, BOOL flag);

void native_host_arm7_arm_03800414(int playerNo, u32 tick);

void native_host_arm7_arm_038004e0(int playerNo, u32 trackBitMask, SNDSeqMute mute);

void native_host_arm7_arm_0380054c(int playerNo, u32 trackBitMask, u32 chBitMask);

void native_host_arm7_arm_038005bc(const void * start, const void * end);

void native_host_arm7_arm_03800648(const void * start, const void * end);

void native_host_arm7_arm_038006a4(int playerNo, u32 offset, u32 data, int size);

void native_host_arm7_arm_038006e8(int playerNo, u32 trackBitMask, u32 offset, u32 data, int size);

typedef enum {
        SND_CAPTURE_0,
        SND_CAPTURE_1
    } SNDCapture;

typedef enum {
	SND_CAPTURE_FORMAT_PCM16,
	SND_CAPTURE_FORMAT_PCM8
} SNDCaptureFormat;
