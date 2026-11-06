typedef	struct {
	u32					workingMemAdrs;
	void*				stack;
	u32					stacksize;
	u32					priority;
	OSMessageQueue*		sendMsgQueuep;
	OSMessageQueue*		recvMsgQueuep;
	u32					dmaChannel;
	u32					dmaMaxSize;
	u32					heapType;
	union
	{
		struct
		{
			OSArenaId		id;
			OSHeapHandle	heapHandle;
		} os;
		struct
		{
			u32	(*alloc)(u32 size);
			u32	(*free)(void* p);
		} ext;
	} heapFunc;
	void*				camAdrs;
	u32					camSize;
} WlInit;

u32       native_utility_child_arm7_arm_027e8b78(WlInit* init);

typedef struct WmInit {
    u32     dmaNo;
    u32     indPrio_low;
    u32     indPrio_high;
    u32     reqPrio_low;
    u32     reqPrio_high;
    u32     wlPrio_low;
    u32     wlPrio_high;
} WmInit;

void    native_utility_child_arm7_main_027e0724(WlInit *wlInit, WmInit *wmInit);

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

void native_utility_child_arm7_arm_027e1fb8(void *arg);

void native_utility_child_arm7_arm_027e2058(void *arg);

extern WMSPWork native_utility_child_arm7_data_027f84f0;

extern OSThread native_utility_child_arm7_data_038091c8;

extern OSThread native_utility_child_arm7_data_0380926c;

static void native_utility_child_arm7_arm_027e0630(PXIFifoTag tag, u32 data, BOOL err);
