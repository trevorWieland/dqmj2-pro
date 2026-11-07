typedef enum {
	SND_CAPTURE_IN_MIXER,
	SND_CAPTURE_IN_CHANNEL,
	SND_CAPTURE_IN_MIXER_L  = SND_CAPTURE_IN_MIXER,
	SND_CAPTURE_IN_MIXER_R  = SND_CAPTURE_IN_MIXER,
	SND_CAPTURE_IN_CHANNEL0 = SND_CAPTURE_IN_CHANNEL,
	SND_CAPTURE_IN_CHANNEL2 = SND_CAPTURE_IN_CHANNEL
} SNDCaptureIn;

typedef enum {
	SND_CAPTURE_OUT_NORMAL,
	SND_CAPTURE_OUT_CHANNEL_MIX,
	SND_CAPTURE_OUT_CHANNEL0_MIX = SND_CAPTURE_OUT_CHANNEL_MIX,
	SND_CAPTURE_OUT_CHANNEL2_MIX = SND_CAPTURE_OUT_CHANNEL_MIX
} SNDCaptureOut;

static inline void SND_StartCapture (SNDCapture capture)
        {
            REGType8v * reg = (REGType8v *)((0x04000000 + 0x508) + capture);
            *reg |= 0x80 ;
        }

static inline void SND_StartCaptureBoth (void)
        {
            (*( REGType16v *) (0x04000000 + 0x508)) |= 0x0080 | 0x8000 ;
        }

static inline void SND_StopCapture (SNDCapture capture)
        {
            (*(REGType8v *)((0x04000000 + 0x508) + capture)) = 0;
        }

void native_host_arm7_arm_037ff0fc(SNDCapture capture, SNDCaptureFormat format, void * buffer_addr, int length, BOOL repeat, SNDCaptureIn in, SNDCaptureOut out);

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

void native_host_arm7_arm_03801d50(int alarmNo, OSTick tick, OSTick period, int id);

void native_host_arm7_arm_03801dac(int alarmNo);

void native_host_arm7_arm_03801e68(int alarmNo);

typedef struct SNDWork {
	SNDExChannel channel[16 ];
	SNDPlayer player[16 ];
	SNDTrack track[32 ];
	SNDAlarm alarm[8 ];
} SNDWork;

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

typedef struct SNDDriverInfo {
	SNDWork work;
	u32 chCtrl[16 ];
	SNDWork * workAddress;
	u32 lockedChannels;
	u32 padding[6];
} SNDDriverInfo;

extern SNDSharedWork * native_host_arm7_data_03807edc;

extern SNDWork native_host_arm7_data_03807ee0;

void native_host_arm7_arm_03801c50(int playerNo, int varNo, s16 var);

void native_host_arm7_arm_03801c70(int varNo, s16 var);

void native_host_arm7_arm_03801c8c(void);

typedef enum SNDChannelOut {
	SND_CHANNEL_OUT_MIXER,
	SND_CHANNEL_OUT_BYPASS
} SNDChannelOut;

typedef enum SNDOutput {
	SND_OUTPUT_MIXER,
	SND_OUTPUT_CHANNEL1,
	SND_OUTPUT_CHANNEL3,
	SND_OUTPUT_CHANNEL1_3
} SNDOutput;

void native_host_arm7_arm_037fe7bc(int volume);

void native_host_arm7_arm_037fe7cc(SNDOutput left, SNDOutput right, SNDChannelOut channel1, SNDChannelOut channel3);

extern OSMessageQueue native_host_arm7_data_03809060;

static void SetChannelTimer(u32 chBitMask, int timer);

static void SetChannelVolume(u32 chBitMask, int volume, SNDChannelDataShift shift);

static void SetChannelPan(u32 chBitMask, int pan);

static void StartTimer(u32 chBitMask, u32 capBitMask, u32 alarmBitMask, u32 flags);

static void StopTimer(u32 chBitMask, u32 capBitMask, u32 alarmBitMask, u32 flags);

static void ReadDriverInfo(SNDDriverInfo * info);
