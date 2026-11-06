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

void native_host_arm7_main_027e5dc0(void *arg);

 void native_host_arm7_main_027e5e80(void *arg);

static void WmspSetVAlarm(s16 count, OSVAlarmHandler handler, void *arg);

static void WmspExpendVRemain(void);

static void WmspSetVAlarm(s16 count, OSVAlarmHandler handler, void *arg)
{
    native_host_arm7_arm_037fd898(&native_host_arm7_data_0380b4bc, count, (192 + 71) , handler, arg);
}

static void WmspExpendVRemain(void)
{
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    s32 vcount = GX_GetVCount();
    s32 i;
    if (208 <= vcount && vcount < 210 ) {
        if (status->v_remain >= ((u32)(1000000ULL * (2) * (256 + 99) * 6 / 33513982)) ) {
            for (i = 1; i < 7; i++) {
                if (status->v_remain < ((u32)(1000000ULL * (2) * (256 + 99) * 6 / 33513982)) + ((u32)(1000000ULL * (1) * (256 + 99) * 6 / 33513982)) * i) {
                    break;
                }
            }
            GX_SetVCount(vcount + (1 - i));
            status->v_remain -= ((u32)(1000000ULL * (1) * (256 + 99) * 6 / 33513982)) * i;
            ((void)0) ;
        }
    }
}
