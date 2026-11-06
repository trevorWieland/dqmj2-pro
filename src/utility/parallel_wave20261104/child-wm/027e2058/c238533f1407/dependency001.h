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

typedef void (*WMSPRequestFunc)(OSMessage msg);

void native_utility_child_arm7_main_027e2058(void *arg);

void WMSP_Initialize(OSMessage msg);

void WMSP_Reset(OSMessage msg);

void WMSP_End(OSMessage msg);

void WMSP_Enable(OSMessage msg);

void WMSP_Disable(OSMessage msg);

void WMSP_PowerOn(OSMessage msg);

void WMSP_PowerOff(OSMessage msg);

void WMSP_SetParentParam(OSMessage msg);

void WMSP_StartParent(OSMessage msg);

void WMSP_EndParent(OSMessage msg);

void WMSP_StartScan(OSMessage msg);

void WMSP_EndScan(OSMessage msg);

void WMSP_StartConnectEx(OSMessage msg);

void WMSP_Disconnect(OSMessage msg);

void WMSP_StartMP(OSMessage msg);

void WMSP_SetMPData(OSMessage msg);

void WMSP_EndMP(OSMessage msg);

void WMSP_StartDCF(OSMessage msg);

void WMSP_SetDCFData(OSMessage msg);

void WMSP_EndDCF(OSMessage msg);

void WMSP_SetWEPKey(OSMessage msg);

void WMSP_SetGameInfo(OSMessage msg);

void WMSP_SetBeaconTxRxInd(OSMessage msg);

void WMSP_StartTestMode(OSMessage msg);

void WMSP_StopTestMode(OSMessage msg);

void WMSP_VAlarmSetMPData(OSMessage msg);

void WMSP_SetLifeTime(OSMessage msg);

void WMSP_MeasureChannel(OSMessage msg);

void WMSP_InitWirelessCounter(OSMessage msg);

void WMSP_GetWirelessCounter(OSMessage msg);

void WMSP_SetEntry(OSMessage msg);

void WMSP_AutoDeAuth(OSMessage msg);

void WMSP_SetMPParameter(OSMessage msg);

void WMSP_AutoDisconnect(OSMessage msg);

void WMSP_KickNextMP_Parent(OSMessage msg);

void WMSP_KickNextMP_Child(OSMessage msg);

void WMSP_KickNextMP_Resume(OSMessage msg);

void WMSP_SetBeaconPeriod(OSMessage msg);

void WMSP_StartScanEx(OSMessage msg);

void WMSP_SetWEPKeyEx(OSMessage msg);

void WMSP_SetPowerSaveMode(OSMessage msg);

void WMSP_StartTestRxMode(OSMessage msg);

void WMSP_StopTestRxMode(OSMessage msg);

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_utility_child_arm7_data_027f84f0;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_utility_child_arm7_data_027f84f0.status;
}

static void WmspRequestFuncDummy(OSMessage msg);

extern const WMSPRequestFunc native_utility_child_arm7_data_027f7df8[WM_APIID_ASYNC_KIND_MAX];
