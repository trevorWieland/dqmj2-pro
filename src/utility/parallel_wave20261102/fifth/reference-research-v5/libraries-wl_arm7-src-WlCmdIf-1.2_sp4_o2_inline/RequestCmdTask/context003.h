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

u16 MLME_ResetReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_PwrMgtReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_ScanReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_JoinReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_AuthReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_DeAuthReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_AssReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_ReAssReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_DisAssReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_StartReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MLME_MeasChanReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

void SendMessageToWmDirect(LPHEAPBUF_MAN pBufMan, void *pMsg);

void RequestCmdTask(void);

typedef struct {
    u8 *pCmd;
    u16 Busy;
    u16 pad;
} CMDIF_MAN, *LPCMDIF_MAN;

typedef struct {
    u16 RequestMinLength;
    u16 ConfirmMinLength;
    u16 (*pCmdFunc)(WlCmdReq *pReq, WlCmdCfm *pCfm);
} WLLIB_CMD_TBL, *LPWLLIB_CMD_TBL;

u16 CMD_ReservedReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

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

typedef WlApElement AP_LIST;

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

u16 MA_DataReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MA_KeyDataReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MA_MpReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MA_TestDataReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 MA_ClrDataReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_AllReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_MacAdrsReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_RetryReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_EnableChannelReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_ModeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_RateReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_WepModeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_WepKeyIdReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_WepKeyReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_BeaconTypeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_ResBcSsidReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_BeaconLostThReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_ActiveZoneReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_SSIDMaskReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_PreambleTypeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_AuthAlgoReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_CCAModeEDThReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_LifeTimeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_MaxConnReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_MainAntennaReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_DiversityReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_BcnSendRecvIndReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_NullKeyModeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_BSSIDReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_SSIDReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_BeaconPeriodReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_DTIMPeriodReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_ListenIntervalReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_GameInfoReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_AllReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_MacAdrsReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_RetryReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_EnableChannelReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_ModeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_RateReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_WepModeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_WepKeyIdReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_BeaconTypeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_ResBcSsidReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_BeaconLostThReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_ActiveZoneReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_SSIDMaskReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_PreambleTypeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_AuthAlgoReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_CCAModeEDThReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_MaxConnReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_MainAntennaReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_DiversityReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_BcnSendRecvIndReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_NullKeyModeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_BSSIDReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_SSIDReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_BeaconPeriodReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_DTIMPeriodReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_ListenIntervalReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMGET_GameInfoReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_ShutdownReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_IdleReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_Class1ReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_RebootReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_ClearWlInfoReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_GetVerInfoReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_GetWlInfoReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_GetStateReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_TestSignalReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 DEV_TestRxReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

static const WLLIB_CMD_TBL WlibCmdTbl_MLME[] = {
    { ((sizeof(WlMlmeResetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmeResetCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_ResetReqCmd },
    { ((sizeof(WlMlmePowerMgtReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmePowerMgtCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_PwrMgtReqCmd },
    { (((sizeof(WlMlmeScanReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) - 3) , (((sizeof(WlMlmeScanCfm) - sizeof(WlCmdHeader) + 1) / 2) - 4 / 2) , MLME_ScanReqCmd },
    { (((sizeof(WlMlmeJoinReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) - 4 / 2) , ((sizeof(WlMlmeJoinCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_JoinReqCmd },
    { ((sizeof(WlMlmeAuthReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmeAuthCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_AuthReqCmd },
    { ((sizeof(WlMlmeDeAuthReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmeDeAuthCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_DeAuthReqCmd },
    { ((sizeof(WlMlmeAssReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmeAssCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_AssReqCmd },
    { ((sizeof(WlMlmeReAssReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmeReAssCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_ReAssReqCmd },
    { ((sizeof(WlMlmeDisAssReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmeDisAssCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_DisAssReqCmd },
    { (((sizeof(WlMlmeStartReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) - 1) , ((sizeof(WlMlmeStartCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_StartReqCmd },
    { ((sizeof(WlMlmeMeasChanReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMlmeMeasChanCfm) - sizeof(WlCmdHeader) + 1) / 2) , MLME_MeasChanReqCmd },
};

static const WLLIB_CMD_TBL WlibCmdTbl_MA[] = {
    { ((sizeof(WlMaDataReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMaDataCfm) - sizeof(WlCmdHeader) + 1) / 2) , MA_DataReqCmd },
    { ((sizeof(WlMaKeyDataReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMaKeyDataCfm) - sizeof(WlCmdHeader) + 1) / 2) , MA_KeyDataReqCmd },
    { ((sizeof(WlMaMpReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMaMpCfm) - sizeof(WlCmdHeader) + 1) / 2) , MA_MpReqCmd },
    { ((sizeof(WlMaTestDataReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMaTestDataCfm) - sizeof(WlCmdHeader) + 1) / 2) , MA_TestDataReqCmd },
    { ((sizeof(WlMaClrDataReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlMaClrDataCfm) - sizeof(WlCmdHeader) + 1) / 2) , MA_ClrDataReqCmd },
};

static const WLLIB_CMD_TBL WlibCmdTbl_PARAMSET[] = {
    { ((sizeof(WlParamSetAllReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_AllReqCmd },
    { ((sizeof(WlParamSetMacAdrsReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_MacAdrsReqCmd },
    { ((sizeof(WlParamSetRetryLimitReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_RetryReqCmd },
    { ((sizeof(WlParamSetEnableChannelReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_EnableChannelReqCmd },
    { ((sizeof(WlParamSetModeReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_ModeReqCmd },
    { ((sizeof(WlParamSetRateReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_RateReqCmd },
    { ((sizeof(WlParamSetWepModeReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_WepModeReqCmd },
    { ((sizeof(WlParamSetWepKeyIdReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_WepKeyIdReqCmd },
    { ((sizeof(WlParamSetWepKeyReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_WepKeyReqCmd },
    { ((sizeof(WlParamSetBeaconTypeReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_BeaconTypeReqCmd },
    { ((sizeof(WlParamSetProbeResReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_ResBcSsidReqCmd },
    { ((sizeof(WlParamSetBeaconLostThReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_BeaconLostThReqCmd },
    { ((sizeof(WlParamSetActiveZoneReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_ActiveZoneReqCmd },
    { ((sizeof(WlParamSetSsidMaskReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_SSIDMaskReqCmd },
    { ((sizeof(WlParamSetPreambleTypeReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_PreambleTypeReqCmd },
    { ((sizeof(WlParamSetAuthAlgoReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_AuthAlgoReqCmd },
    { ((sizeof(WlParamSetCCAModeEDThReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_CCAModeEDThReqCmd },
    { ((sizeof(WlParamSetLifeTimeReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_LifeTimeReqCmd },
    { ((sizeof(WlParamSetMaxConnReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_MaxConnReqCmd },
    { ((sizeof(WlParamSetMainAntennaReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_MainAntennaReqCmd },
    { ((sizeof(WlParamSetDiversityReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_DiversityReqCmd },
    { ((sizeof(WlParamSetBeaconSendRecvIndReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_BcnSendRecvIndReqCmd },
    { ((sizeof(WlParamSetNullKeyModeReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_NullKeyModeReqCmd },
};

static const WLLIB_CMD_TBL WlibCmdTbl_PARAMSET2[] = {
    { ((sizeof(WlParamSetBssidReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_BSSIDReqCmd },
    { ((sizeof(WlParamSetSsidReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_SSIDReqCmd },
    { ((sizeof(WlParamSetBeaconPeriodReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_BeaconPeriodReqCmd },
    { ((sizeof(WlParamSetDtimPeriodReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_DTIMPeriodReqCmd },
    { ((sizeof(WlParamSetIntervalReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_ListenIntervalReqCmd },
    { (((sizeof(WlParamSetGameInfoReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) - 2) , ((sizeof(WlParamSetCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMSET_GameInfoReqCmd },
};

static const WLLIB_CMD_TBL WlibCmdTbl_PARAMGET[] = {
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetAllCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_AllReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetMacAdrsCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_MacAdrsReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetRetryLimitCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_RetryReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetEnableChannelCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_EnableChannelReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetModeCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_ModeReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetRateCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_RateReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetWepModeCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_WepModeReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetWepKeyIdCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_WepKeyIdReqCmd },
    { 0 , 1 , CMD_ReservedReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetBeaconTypeCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_BeaconTypeReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetProbeResCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_ResBcSsidReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetBeaconLostThCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_BeaconLostThReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetActiveZoneCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_ActiveZoneReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetSsidMaskCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_SSIDMaskReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetPreambleTypeCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_PreambleTypeReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetAuthAlgoCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_AuthAlgoReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetCCAModeEDThCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_CCAModeEDThReqCmd },
    { 0 , 1 , CMD_ReservedReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetMaxConnCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_MaxConnReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetMainAntennaCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_MainAntennaReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetDiversityCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_DiversityReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetBeaconSendRecvIndCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_BcnSendRecvIndReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetNullKeyModeCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_NullKeyModeReqCmd },
};

static const WLLIB_CMD_TBL WlibCmdTbl_PARAMGET2[] = {
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetBssidCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_BSSIDReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetSsidCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_SSIDReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetBeaconPeriodCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_BeaconPeriodReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetDtimPeriodCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_DTIMPeriodReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlParamGetIntervalCfm) - sizeof(WlCmdHeader) + 1) / 2) , PARAMGET_ListenIntervalReqCmd },
    { ((sizeof(WlParamGetReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , (((sizeof(WlParamGetGameInfoCfm) - sizeof(WlCmdHeader) + 1) / 2) - 2) , PARAMGET_GameInfoReqCmd },
};

static const WLLIB_CMD_TBL WlibCmdTbl_DEV[] = {
    { 0 , 1 , CMD_ReservedReqCmd },
    { ((sizeof(WlDevShutdownReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevShutdownCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_ShutdownReqCmd },
    { ((sizeof(WlDevIdleReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevIdleCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_IdleReqCmd },
    { ((sizeof(WlDevClass1Req) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevClass1Cfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_Class1ReqCmd },
    { ((sizeof(WlDevRebootReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevRebootCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_RebootReqCmd },
    { ((sizeof(WlDevClrInfoReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevClrInfoCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_ClearWlInfoReqCmd },
    { ((sizeof(WlDevGetVerInfoReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevGetVerInfoCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_GetVerInfoReqCmd },
    { ((sizeof(WlDevGetInfoReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevGetInfoCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_GetWlInfoReqCmd },
    { ((sizeof(WlDevGetStateReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevGetStateCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_GetStateReqCmd },
    { ((sizeof(WlDevTestSignalReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevTestSignalCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_TestSignalReqCmd },
    { ((sizeof(WlDevTestRxReq) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) , ((sizeof(WlDevTestRxCfm) - sizeof(WlCmdHeader) + 1) / 2) , DEV_TestRxReqCmd },
};
