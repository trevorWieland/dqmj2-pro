typedef struct WMCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
} WMCallback;

extern const u16 (*ctrdgi_fl_maxtime);

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlMlmeResetCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				peerMacAdrs[3];
} WlMlmeDeAuthCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
} WlDevIdleCfm;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				buf[2];
} WlCmdCfm;

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

typedef WlMlmeDeAuthCfm WlMlmeDeAuthenticateCfm;

void native_utility_child_arm7_arm_038057c8(void *ptr);

void *native_utility_child_arm7_arm_0380576c(void);

void native_utility_child_arm7_arm_027e4b28(BOOL parent, u16 aid, void *mac);

void native_utility_child_arm7_arm_027e0100(void);

void native_utility_child_arm7_main_027e37f8(OSMessage msg);

WlMlmeResetCfm *native_utility_child_arm7_arm_027e2de4(u16 *buf, u16 mib);

WlMlmeDeAuthenticateCfm *native_utility_child_arm7_arm_027e2b38(u16 *buf, u16 *peerMacAdrs, u16 reasonCode);

WlDevIdleCfm *native_utility_child_arm7_arm_027e2250(u16 *buf);

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}

static void native_utility_child_arm7_arm_027e37bc(u16 wlCommand, u16 wlResult);
