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
    LowestIdleTask,
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

void InitializeTask(void)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    u32 i;
    ;
    pTaskMan->NextPri = 0;
    pTaskMan->TaskPri = 0;
    for (i = 0; i < 4 ; i++) {
        pTaskMan->EnQ[i] = pTaskMan->DeQ[i] = 0xFFFF ;
    }
    for (i = 0; i < sizeof(pTaskFunc) / 4; i++) {
        pTaskMan->TaskTbl[i].NextId = 0xFFFF ;
        pTaskMan->TaskTbl[i].Flag = 0x0000 ;
        pTaskMan->TaskTbl[i].pTaskFunc = pTaskFunc[i];
    }
    AddTask(3 , 12 );
}

void MainTaskRoutine(void *arg)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    u32 x;
    pTaskMan->NextPri = 0;
    pTaskMan->CurrTaskID = 0;
    ;
    while (1) {
        OSMessage msg;
        if (OS_ReceiveMessage(((LPWL_MAN)native_host_arm7_data_0380fff4) ->pRecvMsgQueue, &msg, 0 )) {
            ExecuteMessage(&msg);
        }
        x = OS_DisableIrqMask((1UL << 24) | (1UL << 4) );
        pTaskMan->TaskPri = pTaskMan->NextPri;
        if (pTaskMan->EnQ[pTaskMan->TaskPri] == 0xFFFF ) {
            ++pTaskMan->NextPri;
            OS_EnableIrqMask(x);
        } else {
            OS_EnableIrqMask(x);
            pTaskMan->CurrTaskID = (u16)DeleteTask(pTaskMan->TaskPri);
            ;
            (*pTaskMan->TaskTbl[pTaskMan->CurrTaskID].pTaskFunc)();
            ;
            pTaskMan->CurrTaskID = 0xFFFF ;
        }
    }
}

void AddTask(s32 nPriority, u32 nTaskID)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    LPTASK_TBL pTaskTbl;
    u32 x;
    ;
    pTaskTbl = pTaskMan->TaskTbl;
    x = OS_DisableIrqMask((1UL << 24) | (1UL << 4) );
    if (pTaskTbl[nTaskID].Flag == 0x0000 ) {
        pTaskTbl[nTaskID].Flag = 0x0001 ;
        pTaskTbl[nTaskID].NextId = 0xFFFF ;
        if (pTaskMan->DeQ[nPriority] == 0xFFFF ) {
            pTaskMan->EnQ[nPriority] = (u16)nTaskID;
        } else {
            pTaskMan->TaskTbl[pTaskMan->DeQ[nPriority]].NextId = (u16)nTaskID;
        }
        pTaskMan->DeQ[nPriority] = (u16)nTaskID;
        if (nPriority < pTaskMan->NextPri) {
            pTaskMan->NextPri = (u16)nPriority;
        }
    }
    OS_EnableIrqMask(x);
    if ((nPriority != 3 ) && (pTaskMan->TaskPri == 3 )) {
        OS_SendMessage(((LPWL_MAN)native_host_arm7_data_0380fff4) ->pRecvMsgQueue, 0 , 0 );
    }
}

u32 DeleteTask(u32 nPriority)
{
    LPTASK_MAN pTaskMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    LPTASK_TBL pTaskTbl;
    u32 x, nTaskID, nOfstTaskID;
    x = OS_DisableIrqMask((1UL << 24) | (1UL << 4) );
    if ((nTaskID = pTaskMan->EnQ[nPriority]) != 0xFFFF ) {
        pTaskTbl = pTaskMan->TaskTbl;
        nOfstTaskID = nTaskID;
        pTaskTbl[nOfstTaskID].Flag = 0x0000 ;
        if (pTaskTbl[nOfstTaskID].NextId == 0xFFFF ) {
            pTaskMan->EnQ[nPriority] = 0xFFFF ;
            pTaskMan->DeQ[nPriority] = 0xFFFF ;
        } else {
            pTaskMan->EnQ[nPriority] = pTaskTbl[nOfstTaskID].NextId;
            pTaskTbl[nOfstTaskID].NextId = 0xFFFF ;
        }
    }
    OS_EnableIrqMask(x);
    return nTaskID;
}

void LowestIdleTask(void)
{
    OSMessage msg;
    OS_ReceiveMessage(((LPWL_MAN)native_host_arm7_data_0380fff4) ->pRecvMsgQueue, &msg, 1 );
    ExecuteMessage(&msg);
    AddTask(3 , 12 );
}

void ExecuteMessage(OSMessage *pMsg)
{
    if (*pMsg != 0 ) {
        WlCmdReq *pReq = (WlCmdReq *)*pMsg;
        NewHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.RequestCmd, *pMsg);
        AddTask(2 , 11 );
    }
}
