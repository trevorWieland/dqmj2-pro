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

void native_host_arm7_arm_038073a4(void *ptr);

void *native_host_arm7_arm_038073f0(void);

BOOL native_host_arm7_arm_027e02ac(const u8 *macAdr);

BOOL native_host_arm7_arm_027e74f8(BOOL timeout, u16 pollBitmap);

void native_host_arm7_arm_027e7828(u16 aidBitmap);

void native_host_arm7_arm_027e7a1c(u16 aid, u16 wmHeader, u16 *data, u16 length, WMMpRecvBuf *recvBuf);

void native_host_arm7_arm_027e0520(u8 rssi8);

u16 native_host_arm7_arm_027e059c(void);

void native_host_arm7_arm_027e0640(void);

void native_host_arm7_arm_027e076c(void);

void native_host_arm7_arm_027e086c(u16 childMaxSize);

void native_host_arm7_arm_027e1a54(void);

void native_host_arm7_main_027e0898(void *arg);

u32 *native_host_arm7_arm_027e0700(void);

void native_host_arm7_arm_027e5b98(void);

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_host_arm7_data_027f7884;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_host_arm7_data_027f7884.status;
}

inline u8 native_host_arm7_arm_027e1a40(u8 rssi);

static inline void WMSP_AddRssiToRandomPool(u8 rssi8)
{
    u32 rssi_pool = (u32)(((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool << 1);
    rssi_pool ^= rssi8;
    rssi_pool ^= rssi_pool >> 16;
    ((OSSystemWork *)(0x02000000 + 0x007ffc00)) ->wm_rssi_pool = (u16)rssi_pool;
}

extern OSAlarm native_host_arm7_data_0380b490;

extern OSAlarm native_host_arm7_data_0380b464;

static void WmspIndicate(WlCmdReq *req);

static void native_host_arm7_arm_027e1a08(WlCmdReq *buf);

static void WmspIndicateFuncDummy(WlCmdReq *req);

static void WmspIndicateMlmeBeaconSend(WlCmdReq *req);

static void WmspIndicateMlmeBeaconRecv(WlCmdReq *req);

static void WmspIndicateMlmeBeaconLost(WlCmdReq *req);

static void WmspIndicateMaMultiPollEnd(WlCmdReq *req);

static void WmspIndicateMaMultiPoll(WlCmdReq *req);

static void WmspIndicateMaMultiPollAck(WlCmdReq *req);

static void WmspIndicateMaData(WlCmdReq *req);

static void WmspIndicateMaFatalErr(WlCmdReq *req);

static void WmspIndicateMlmeDisAssociate(WlCmdReq *req);

static void WmspIndicateMlmeReAssociate(WlCmdReq *req);

static void WmspIndicateMlmeAssociate(WlCmdReq *req);

static void WmspIndicateMlmeDeAuthenticate(WlCmdReq *req);

static void WmspIndicateMlmeAuthenticate(WlCmdReq *req);

static void native_host_arm7_arm_027e1b68(void *arg);

static void WmspSetRssi(WlMaMpEndInd *pInd, u16 pollBitmap, BOOL minPollBmpMode);

static void native_host_arm7_arm_027e1ad4(void *arg);

static void native_host_arm7_arm_027e1ae8(u16 pollbmp);

static void native_host_arm7_arm_027e1c00(void *arg);

static void native_host_arm7_arm_027e1c0c(void);

static void WmspCancelMPIntervalAlarm(void);

static void WmspCancelMPAckAlarm(void);

static inline BOOL WMSPi_IsChild(u32 stat)
{
    return (stat == WM_STATE_MP_CHILD) || (stat == WM_STATE_CHILD);
}

static inline BOOL WMSPi_IsParent(u32 stat)
{
    return (stat == WM_STATE_MP_PARENT) || (stat == WM_STATE_PARENT);
}

static inline void WmspCancelMPAckAlarm(void)
{
    native_host_arm7_arm_037fd5c0(&native_host_arm7_data_0380b464);
}

static inline void WmspCancelMPIntervalAlarm(void)
{
    native_host_arm7_arm_037fd5c0(&native_host_arm7_data_0380b490);
}
