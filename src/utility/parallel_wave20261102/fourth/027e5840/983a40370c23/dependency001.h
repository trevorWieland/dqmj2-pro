typedef	struct {
	u16			frameId;
	u8			rsv1[4];
	u16			length;
	u16			status;
	u16			rsvm1;
	u16			rsvm2;
	u8			rate;
	u8			rssi;
	u32			rsvm3;
	u8			rsv4[4];
	u16			destAdrs[3];
	u16			srcAdrs[3];
	u8			rsv5[8];
	u16*		datap;
} WlTxFrame;

typedef	struct {
	u16		code;
	u16		length;
} WlCmdHeader;

typedef	struct {
	WlCmdHeader		header;
	u16				resultCode;
	u16				txStatus;
} WlMaDataCfm;

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

void native_utility_child_arm7_arm_038057c8(void *ptr);

void *native_utility_child_arm7_arm_0380576c(void);

void native_utility_child_arm7_main_027e5840(OSMessage msg);

WlMaDataCfm *native_utility_child_arm7_arm_027e28a0(u16 *buf, WlTxFrame *frame);

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}
