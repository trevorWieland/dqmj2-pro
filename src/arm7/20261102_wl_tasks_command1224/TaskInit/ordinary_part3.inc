    u16 CurrChannel;
    u16 CapaInfo;
    u16 BeaconLostTh;
    u16 BeaconLostCnt;
    u16 LinkAdrs[3];
    u16 APCamAdrs;
    u16 FrameCtrl;
    u16 FrameLifeTime;
    u16 bExistTIM;
    u16 TxPower;
    struct {
        struct {
            u16 SSID;
            u16 TIM;
            u16 GameInfo;
        } Beacon;
        struct {
            u16 SSID;
        } ProbeReq;
        struct {
            u16 Size;
        } RxBuf;
    } Ofst;
    void *GameInfoAdrs;
    u16 GameInfoLength;
    u16 GameInfoAlign;
    u16 bUpdateGameInfo;
    u16 TmpttPs;
    u32 IntervalCount;
    u16 Scrambler;
    u16 DbgSeqNum;
    u16 FatalErr;
    u16 rsv;
    u16 CurrErrCount;
    u16 TxBufErrCount;
    u16 TxBufResCount;
    u16 WepErrCount;
    u16 MpEndErrCount;
    u16 NotPollTxErrCount;
} WORK_PARAM, *LPWORK_PARAM;


typedef struct {
    u16 a;
    u16 b;
    u16 seed;
    u16 rsv;
} RAND_CTRL, *LPRAND_CTRL;


typedef struct {
    u16 Id;
    u16 Bits;
    u16 InitNum;
    u16 ChanNum;
    u16 BbpCnt;
    u16 pad;
    u32 BkReg;
} RF_CONFIG, *LPRF_CONFIG;


void SendFatalErrMsgTask(void);


void TerminateWlTask(void);


void ReleaseWlTask(void);


typedef struct {
    u16 State;
    u16 pad;
    union {
        struct {
            u16 MaxConfirmLength;
            u16 ChannelCount;
            u16 bFound;
            u16 ElapseTime;
            u16 TxPeriod;
        } Scan;
        struct {
            u16 Result;
            u16 Status;
        } Join;
        struct {
            LPTXFRM pTxFrm;
        } DeAuth;
        struct {
            LPTXFRM pTxFrm;
        } DisAss;
        struct {
            u32 Counter;
            u32 CCA;
            u16 bkPowerMode;
            u16 bkCCAMode;
            u16 bkEdTh;
            u16 bkMode;
            u16 Channel;
            u16 sts;
        } Measure;
    } Work;
    union {
        WlMlmeResetReq *Reset;
        WlMlmePowerMgtReq *PwrMgt;
        WlMlmeScanReq *Scan;
        WlMlmeJoinReq *Join;
        WlMlmeAuthReq *Auth;
        WlMlmeDeAuthReq *DeAuth;
        WlMlmeAssReq *Ass;
        WlMlmeReAssReq *ReAss;
        WlMlmeDisAssReq *DisAss;
        WlMlmeStartReq *Start;
        WlMlmeMeasChanReq *MeasChannel;
    } pReq;
    union {
        WlCmdCfm *Cfm;
        WlMlmeResetCfm *Reset;
        WlMlmePowerMgtCfm *PwrMgt;
        WlMlmeScanCfm *Scan;
        WlMlmeJoinCfm *Join;
        WlMlmeAuthCfm *Auth;
        WlMlmeDeAuthCfm *DeAuth;
        WlMlmeAssCfm *Ass;
        WlMlmeReAssCfm *ReAss;
        WlMlmeDisAssCfm *DisAss;
        WlMlmeStartCfm *Start;
        WlMlmeMeasChanCfm *MeasChannel;
    } pCfm;
} MLME_MAN, *LPMLME_MAN;


void MLME_ScanTask(void);


void MLME_JoinTask(void);


void MLME_AuthTask(void);


void MLME_AssTask(void);


void MLME_ReAssTask(void);


void MLME_MeasChannelTask(void);


void MLME_BeaconLostTask(void);


void SendMessageToWmTask(void);


void RequestCmdTask(void);


typedef struct {
    u8 *pCmd;
    u16 Busy;
    u16 pad;
} CMDIF_MAN, *LPCMDIF_MAN;


typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    DATA_HEADER Dot11Header;
    u8 Body[4];
} RXFRM, *LPRXFRM;


typedef struct {
    u16 wlRsv[(12/2) ];
    WlCmdHeader header;
    RXFRM frame;
} RXPACKET, *LPRXPACKET;


typedef struct {
    u16 DA[3];
    u16 SA[3];
    SEQ_CTRL SeqCtrl;
    u16 pad;
} DEFRAG_TBL, *LPDEFRAG_TBL;


typedef struct {
    u16 RestTime;
    u16 UnitLength;
    DEFRAG_TBL DefragTbl;
    LPRXPACKET pPacket;
} DEFRAG_LIST, *LPDEFRAG_LIST;


typedef struct {
    u16 LastMpSeq;
    u16 IcvOkCntFlag;
    u16 wlCurr;
    u16 TxKeyReg;
    DEFRAG_LIST DefragList[3 ];
} RX_CTRL, *LPRX_CTRL;


void RxDataFrameTask(void);


void RxManCtrlTask(void);


void DefragTask(void);


void DefragTimerTask(void);


typedef WlApElement AP_LIST;


void UpdateApListTask(void);


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
extern void (*const native_host_arm7_table_ptaskfunc_027f7248[24])(void);


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
    for (i = 0; i < sizeof(native_host_arm7_table_ptaskfunc_027f7248) / 4; i++) {
        pTaskMan->TaskTbl[i].NextId = 0xFFFF ;
        pTaskMan->TaskTbl[i].Flag = 0x0000 ;
        pTaskMan->TaskTbl[i].native_host_arm7_table_ptaskfunc_027f7248 = native_host_arm7_table_ptaskfunc_027f7248[i];
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
            (*pTaskMan->TaskTbl[pTaskMan->CurrTaskID].native_host_arm7_table_ptaskfunc_027f7248)();
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
