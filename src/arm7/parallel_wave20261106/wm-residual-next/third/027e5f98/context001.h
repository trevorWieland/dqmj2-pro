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

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_host_arm7_data_027f7884;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_host_arm7_data_027f7884.status;
}

extern OSVAlarm native_host_arm7_data_0380b4bc;

void native_host_arm7_main_027e5f98(void *arg);

 void native_host_arm7_arm_027e6050(void *arg);

static void WmspSetVAlarm(s16 count, OSVAlarmHandler handler, void *arg);

static void WmspSetVTSF(void);

static void WmspSetVAlarm(s16 count, OSVAlarmHandler handler, void *arg)
{
    native_host_arm7_arm_037fd898(&native_host_arm7_data_0380b4bc, count, (192 + 71) , handler, arg);
}

static void WmspSetVTSF(void)
{
    u16 vcount;
    u32 cur_tsf;
    u16 low0, low1, high;
    u32 v_tsf;
    vcount = (u16)GX_GetVCount();
    low0 = *(vu16 *)((0x04808000) + 0x0F8) ;
    high = *(vu16 *)((0x04808000) + 0x0FA) ;
    low1 = *(vu16 *)((0x04808000) + 0x0F8) ;
    if (low0 > low1) {
        high = *(vu16 *)((0x04808000) + 0x0FA) ;
    }
    cur_tsf = high;
    cur_tsf <<= 16;
    cur_tsf |= low1;
    v_tsf = cur_tsf;
    v_tsf <<= 1;
    v_tsf -= vcount * 127;
    v_tsf >>= 7;
    v_tsf &= 0x0000ffff;
    *(vu16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) = (u16)v_tsf;
    return;
}
