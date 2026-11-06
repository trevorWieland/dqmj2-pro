extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	u16				wlRsv[(12/2) ];
	WlCmdHeader		header;
	u16				staMacAdrs[3];
	u16				retryLimit;
	u16				enableChannel;
	u16				rsv;
	u16				mode;
	u16				rate;
	u16				wepMode;
	u16				wepKeyId;
	u16				wepKey[4][10];
	u16				beaconType;
	u16				probeRes;
	u16				beaconLostTh;
	u16				activeZoneTime;
	u8				ssidMask[32];
	u16				preambleType;
	u16				authAlgo;
} WlParamSetAllReq;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlParamSetCfm;

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

BOOL native_utility_child_arm7_main_027e03b8(u16 wmApiID, u16 *buf);

WlParamSetCfm *native_utility_child_arm7_arm_027e26e0(WlParamSetAllReq *req);

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_utility_child_arm7_data_027f84f0;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}

extern WMSPWork native_utility_child_arm7_data_027f84f0;

static void native_utility_child_arm7_arm_027e01a4(u16 wmApiID, u16 wlCommand, u16 wlResult);
