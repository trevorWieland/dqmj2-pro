u16 MLME_ReAssReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);


u16 MLME_DisAssReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);


u16 MLME_StartReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);


u16 MLME_MeasChanReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);


void SendMessageToWmDirect(LPHEAPBUF_MAN pBufMan, void *pMsg);


void SendMessageToWmTask(void);


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
extern const WLLIB_CMD_TBL native_host_arm7_table_wlibcmdtbl_mlme_027f7654[11];
extern const WLLIB_CMD_TBL native_host_arm7_table_wlibcmdtbl_ma_027f75cc[5];
extern const WLLIB_CMD_TBL native_host_arm7_table_wlibcmdtbl_paramset_027f77bc[23];
extern const WLLIB_CMD_TBL native_host_arm7_table_wlibcmdtbl_paramset2_027f7624[6];
extern const WLLIB_CMD_TBL native_host_arm7_table_wlibcmdtbl_paramget_027f7704[23];
extern const WLLIB_CMD_TBL native_host_arm7_table_wlibcmdtbl_paramget2_027f75f4[6];
extern const WLLIB_CMD_TBL native_host_arm7_table_wlibcmdtbl_dev_027f76ac[11];


void RequestCmdTask(void)
{
    LPCMDIF_MAN pCmdIf = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->CmdIf;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlCmdReq *pReq;
    WlCmdCfm *pCfm;
    LPWLLIB_CMD_TBL pCmdTbl;
    u16 vCode, vCodeMax, err = 0;
    u16 currBusy = 0;
    if (pCmdIf->Busy) {
        ;
        return;
    }
    pCmdIf->pCmd = (u8 *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.RequestCmd).Head) ;
    if ((u32)pCmdIf->pCmd == (u32)(-1) ) {
        return;
    }
    pReq = (WlCmdReq *)pCmdIf->pCmd;
    pCfm = (WlCmdCfm *)((u32)pReq + ((WlCmdReq*)pReq)->header.length*2 + 12+4) ;
    ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.DiagResult) {
        currBusy = 0;
        pCfm->header.length = 1;
        pCfm->resultCode = 0x06 ;
        goto end_of_command;
    }
    if (pReq->header.code != pCfm->header.code) {
        pCfm->resultCode = 0x0D ;
        goto end_of_command;
    }
    switch (pReq->header.code & 0xFF00 ) {
    case 0x0000 :
        ;
        currBusy = 0x01 ;
        pCmdTbl = (LPWLLIB_CMD_TBL)native_host_arm7_table_wlibcmdtbl_mlme_027f7654;
        vCode = pReq->header.code & 0x00FF ;
        vCodeMax = (sizeof(native_host_arm7_table_wlibcmdtbl_mlme_027f7654) / sizeof(WLLIB_CMD_TBL)) ;
        if (pCmdIf->Busy & 0x01 ) {
            err = 0x02 ;
        }
        else if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA < 0x20 ) {
            err = 0x01 ;
        }
        break;
    case 0x0100 :
        ;
        currBusy = 0x02 ;
        pCmdTbl = (LPWLLIB_CMD_TBL)native_host_arm7_table_wlibcmdtbl_ma_027f75cc;
        vCode = pReq->header.code & 0x00FF ;
        vCodeMax = (sizeof(native_host_arm7_table_wlibcmdtbl_ma_027f75cc) / sizeof(WLLIB_CMD_TBL)) ;
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x40 ) {
            err = 0x01 ;
        }
        break;
    case 0x0200 :
        vCode = pReq->header.code & 0x00FF ;
        if (vCode < ((0x0200 | 0x40) & 0x00FF )) {
            ;
            if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA < 0x10 ) {
                err = 0x01 ;
            }
            currBusy = 0x04 ;
            pCmdTbl = (LPWLLIB_CMD_TBL)native_host_arm7_table_wlibcmdtbl_paramset_027f77bc;
            vCodeMax = (sizeof(native_host_arm7_table_wlibcmdtbl_paramset_027f77bc) / sizeof(WLLIB_CMD_TBL)) ;
        } else if (vCode < ((0x0200 | 0x80) & 0x00FF )) {
            ;
            if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x40 ) {
                err = 0x01 ;
            }
            currBusy = 0x08 ;
