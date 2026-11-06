typedef struct WMArm7Buf {
	WMStatus * status;
	u8 reserved_a[4];
	u32 * fifo7to9;
	u8 reserved_b[4];
	WMBssDesc connectPInfo;
	u32 requestBuf[512 / sizeof(u32)];
} WMArm7Buf, WMarm7Buf;

typedef struct WMPortSendCallback {
	u16 apiid;
	u16 errcode;
	u16 wlCmdID;
	u16 wlResult;
	u16 state;
	u16 port;
	u16 destBitmap;
	u16 restBitmap;
	u16 sentBitmap;
	u16 rsv;
	const u16 * data;
	union {
		u16 size;
		u16 length;
	};
	u16 seqNo;
	WMCallbackFunc callback;
	void * arg;
	u16 maxSendDataSize;
	u16 maxRecvDataSize;
} WMPortSendCallback;

extern const u16 (*ctrdgi_fl_maxtime);

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

int native_utility_child_arm7_arm_027e735c(u32 childBitmap, u16 priority, u16 port, u32 destBitmap, const u16 *sendData, u16 sendDataSize, WMCallbackFunc callback, void *arg);

void native_utility_child_arm7_main_027e5510(OSMessage msg);

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_utility_child_arm7_data_027f84f0;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}
