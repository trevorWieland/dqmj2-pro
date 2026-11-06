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

extern WMSPWork native_host_arm7_data_027f7884;

void native_host_arm7_main_027e0520(u8 rssi8);

static inline void WMSP_AddRssiToRandomPool(u8 rssi8)
{
    u32 rssi_pool = (u32)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool << 1);
    rssi_pool ^= rssi8;
    rssi_pool ^= rssi_pool >> 16;
    ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool = (u16)rssi_pool;
}

extern WMSPWork native_host_arm7_data_027f7884;
