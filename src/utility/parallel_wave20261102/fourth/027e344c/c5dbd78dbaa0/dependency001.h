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

void native_utility_child_arm7_main_027e344c(OSMessage msg);

WlParamSetCfm *native_utility_child_arm7_arm_027e2474(u16 *buf, u16 count);

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}

static void native_utility_child_arm7_arm_027e3410(u16 wlCommand, u16 wlResult);
