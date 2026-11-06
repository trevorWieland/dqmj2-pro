typedef struct {
    TASK_MAN TaskMan;
    HEAP_MAN HeapMan;
    AP_LIST ApList[4 ];
    OSMessageQueue *pSendMsgQueue;
    OSMessageQueue *pRecvMsgQueue;
    u32 DmaChannel;
    u32 DmaMaxCount;
    s32 lockID;
    void *pFlashImg;
    CONFIG_PARAM Config;
    WORK_PARAM Work;
    MLME_MAN MLME;
    CMDIF_MAN CmdIf;
    TX_CTRL TxCtrl;
    RX_CTRL RxCtrl;
    CAM_MAN CamMan;
    WlCounter Counter;
    RAND_CTRL Rand;
    RF_CONFIG Rf;
    OSAlarm PeriodicAlarm;
    OSAlarm Alarm;
    OSAlarm KeyAlarm;
    u32 WlDbgLevel;
    u16 WlOperation;
    u16 EnableChannel;
} WL_MAN, *LPWL_MAN;

void WlIntrTxBeaconTask(void);

void WlIntrTxEndTask(void);

void WlIntrRxEndTask(void);

void WlIntrMpEndTask(void);

void SetParentTbttTxqTask(void);

static void (*const pTaskFunc[])(void) = {
    MLME_ScanTask,
    MLME_JoinTask,
    MLME_AuthTask,
    MLME_AssTask,
    MLME_ReAssTask,
    MLME_MeasChannelTask,
    RxDataFrameTask,
    RxManCtrlTask,
    WlIntrTxBeaconTask,
    DefragTask,
    CAM_TimerTask,
    RequestCmdTask,
    native_utility_child_arm7_wram_037f8690,
    MLME_BeaconLostTask,
    WlIntrTxEndTask,
    WlIntrRxEndTask,
    WlIntrMpEndTask,
    DefragTimerTask,
    UpdateApListTask,
    SendMessageToWmTask,
    SetParentTbttTxqTask,
    SendFatalErrMsgTask,
    TerminateWlTask,
    ReleaseWlTask,
};

void native_utility_child_arm7_arm_037f8558(s32 nPriority, u32 nTaskID);
