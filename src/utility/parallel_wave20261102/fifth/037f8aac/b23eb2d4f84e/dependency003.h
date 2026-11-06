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

void native_utility_child_arm7_arm_037f8dc4(LPHEAPBUF_MAN pBufMan, void *pMsg);

void native_utility_child_arm7_wram_037f8aac(void);

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

extern const WLLIB_CMD_TBL native_utility_child_arm7_data_027f82c0[11];

extern const WLLIB_CMD_TBL native_utility_child_arm7_data_027f8238[5];

extern const WLLIB_CMD_TBL native_utility_child_arm7_data_027f8428[23];

extern const WLLIB_CMD_TBL native_utility_child_arm7_data_027f8290[6];

extern const WLLIB_CMD_TBL native_utility_child_arm7_data_027f8370[23];

extern const WLLIB_CMD_TBL native_utility_child_arm7_data_027f8260[6];

extern const WLLIB_CMD_TBL native_utility_child_arm7_data_027f8318[11];
