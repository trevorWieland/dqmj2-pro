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

typedef WlParamGetMacAdrsCfm WlParamGetMacAddressCfm;

typedef WlDevRebootCfm WlDevRestartCfm;

typedef WlDevGetVerInfoCfm WlDevGetVersionCfm;

u16 native_host_arm7_arm_03807444(u16 bitField);

WlParamSetCfm *native_host_arm7_arm_027e25e0(u16 *buf, u16 tableNumber, u16 camLifeTime, u16 frameLifeTime);

WlParamSetCfm *native_host_arm7_arm_027e26a4(u16 *buf, u16 enableMessage);

WlParamGetMacAddressCfm *native_host_arm7_arm_027e283c(u16 *buf);

WlParamGetEnableChannelCfm *native_host_arm7_arm_027e2854(u16 *buf);

WlDevIdleCfm *native_host_arm7_arm_027e2898(u16 *buf);

WlDevRestartCfm *native_host_arm7_arm_027e28c8(u16 *buf);

WlDevGetVersionCfm *native_host_arm7_arm_027e28f4(u16 *buf);

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_host_arm7_data_027f7884.status;
}

static void WmspStabilizeBeacon(void);

BOOL native_host_arm7_main_027e8110(u16 *pWlCommand, u16 *pWlResult);
