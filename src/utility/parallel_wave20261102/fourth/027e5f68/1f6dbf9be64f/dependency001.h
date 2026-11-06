typedef struct WMMeasureChannelCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 channel;
	u16 ccaBusyRatio;
} WMMeasureChannelCallback, WMmeasureChannelCallback;

static inline void MI_WriteByte (void * address, u8 value)
    {
        *(u8 *)address = value;
    }

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmePowerMgtCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				reserved;
	u16				ccaBusyInfo[16];
} WlMlmeMeasChanCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevIdleCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevClass1Cfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				state;
} WlDevGetStateCfm;

typedef struct WMSPWork {
    OSMessageQueue toWLmsgQ;
    OSMessage toWLmsg[2 ];
    OSMessageQueue fromWLmsgQ;
    OSMessage fromWLmsg[4 ];
    OSMessageQueue confirmQ;
    OSMessage confirm[4 ];
    OSMessageQueue requestQ;
    OSMessage request[32 ];
    u32 requestStack[4096 / sizeof(u32)];
    u32 indicateStack[1024 / sizeof(u32)];
    OSMutex fifoExclusive;
    u32 dmaNo;
    OSArenaId arenaId;
    OSHeapHandle heapHandle;
    WMArm7Buf *wm7buf;
    WMStatus *status;
    u8 rssiHistory[32 ];
    u32 rssiIndex;
    u32 indPrio_high;
    u32 wlPrio_high;
    u32 reqPrio_high;
    u32 indPrio_low;
    u32 wlPrio_low;
    u32 reqPrio_low;
} WMSPWork;

extern WMSPWork native_utility_child_arm7_data_027f84f0;

typedef WlMlmePowerMgtCfm WlMlmePowerManagementCfm;

typedef WlMlmeMeasChanCfm WlMlmeMeasureChannelCfm;

typedef WlDevGetStateCfm WlDevGetStationStateCfm;

void native_utility_child_arm7_arm_038057c8(void *ptr);

void *native_utility_child_arm7_arm_0380576c(void);

BOOL native_utility_child_arm7_arm_027e03b8(u16 wmApiID, u16 *buf);

void native_utility_child_arm7_main_027e5f68(OSMessage msg);

WlMlmePowerManagementCfm *native_utility_child_arm7_arm_027e2d80(u16 *buf, u16 pwrMgtMode, u16 wakeUp, u16 recieveDtims);

WlMlmeMeasureChannelCfm *native_utility_child_arm7_arm_027e2958(u16 *buf, u16 ccaMode, u16 edThreshold, u16 measureTime, u8 *channelList);

WlDevIdleCfm *native_utility_child_arm7_arm_027e2250(u16 *buf);

WlDevClass1Cfm *native_utility_child_arm7_arm_027e2238(u16 *buf);

WlDevGetStationStateCfm *native_utility_child_arm7_arm_027e21c8(u16 *buf);

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}

static void native_utility_child_arm7_arm_027e5f2c(u16 wlCommand, u16 wlResult);
