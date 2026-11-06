void SetManCtrlFrame(LPTXFRM pFrm);

void MakeBeaconFrame(void);

LPDEAUTH_FRAME MakeDeAuthFrame(u16 *pDA, u16 reasonCode, u32 bCheck);

void InitTxCtrl(void);

void TxqEndBroadCast(LPTXFRM pFrm, u32 flag);

void InitManHeader(LPTXFRM pFrm, u16 *pDA);

u32 SetSupRateSet(u8 *pBuf);

typedef WlStaElement *LPCAM_ELEMENT;

typedef struct {
    u16 Count;
    u16 PowerMgtMode;
    u16 PowerState;
    u16 NotClass3;
    u16 NotSetTIM;
    u16 dmm;
    u16 ConnectSta;
    u16 UseAidMap;
} CAM_MAN, *LPCAM_MAN;

u32 CAM_Search(u16 *pMacAdrs);

void CAM_SetStaState(u16 camAdrs, u16 state);

void CAM_SetDoze(u32 camAdrs);

u32 CAM_GetStaState(u32 camAdrs);

u32 CAM_IsActive(u32 camAdrs);

u32 CAM_GetPowerMgtMode(u32 camAdrs);

u32 CAM_GetFrameCount(u32 camAdrs);

void CAM_IncFrameCount(LPTXFRM pFrm);

void CAM_DecFrameCount(LPTXFRM pFrm);

void CAM_ClrTIMElementBitmap(u32 camAdrs);

void CAM_ReleaseAID(u16 camAdrs);

void CAM_Delete(u16 camAdrs);

inline u32 LoadHigh(u16 *p)
{
    return *p >> 8;
}

inline u32 LoadLow(u16 *p)
{
    return *p & 0x00FF;
}

typedef struct {
    u16 Basic;
    u16 Support;
} RATE_SET, *LPRATE_SET;

typedef struct {
    LPCAM_ELEMENT pCAM;
    u16 CamMaxStaNum;
    u16 MaxStaNum;
    u16 MacAdrs[3];
    u16 RetryLimit;
    u16 EnableChannel;
    u16 Mode;
    u16 Rate;
    u16 AuthAlgo;
    u16 WepMode;
    u16 WepKeyId;
    u16 FrameLifeTimePerBeacon;
    u16 BeaconType : 1;
    u16 BcSsidResponse : 1;
    u16 PreambleType : 1;
    u16 MainAntenna : 1;
    u16 Diversity : 1;
    u16 UseAntenna : 1;
    u16 BcnTxRxIndMsg : 1;
    u16 NullKeyRes : 1;
    u16 dmm : 8;
    u16 ActiveZone;
    u16 DiagResult;
    u32 ParamFlag;
} CONFIG_PARAM, *LPCONFIG_PARAM;
typedef struct {
    u64 NextTbttTsf;
    u16 STA;
    u16 RSSI;
    u16 Mode;
    u16 PowerMgtMode;
    u16 PowerState;
    u16 bSynchro;
    u16 RxDtims;
    u16 PN15Rate;
    u16 SigTest2;
    u16 bFirstTbtt;
    u16 ManCtrlRetry;
    u16 SSIDLength;
    u8 SSID[32 ];
    u8 SSIDMask[32 ];
    RATE_SET RateSet;
    u16 BSSID[3];
    u16 AID;
    u16 SeqNum;
    u16 BeaconPeriod;
    u16 ListenInterval;
    u16 CurrListenInterval;
    u16 DTIMPeriod;
    u16 DTIMCount;
    u16 rsvcc;
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

u16 WSetPowerState(u32 state);

void WSetStaState(u32 state);

void WClearAids(void);

void WSetMacAdrs3(u16 *dst, u16 *src1, u16 *src2, u16 *src3);

void WUpdateCounter(void);

u32 WCalcManRate(void);

void DMA_Write(void *destAdrs, void *srcAdrs, u32 length);

void DMA_WriteHeaderData(LPTXFRM_MAC destAdrs, LPMAC_HEADER header, u8 *data, u32 length);

void DMA_WepWriteHeaderData(LPTXFRM_MAC destAdrs, LPMAC_HEADER header, u8 *data, u32 length);

void WL_WriteByte(void *p, u8 data);

u8 WL_ReadByte(void *p);

void SetFatalErr(u32 errCode);

extern const u16 RateBit2Element[];

extern const u16 BC_ADRS[3];

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

void IssueMlmeConfirm(void);

u32 MLME_IssueAuthIndication(u16 *pMacAdrs, u16 algorithm);

u32 MLME_IssueDeAuthIndication(u16 *pMacAdrs, u16 reason);

u32 MLME_IssueAssIndication(u16 *pMacAdrs, u16 aid, LPSSID_ELEMENT pSSID);

u32 MLME_IssueReAssIndication(u16 *pMacAdrs, u16 aid, LPSSID_ELEMENT pSSID);

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

void IssueMaDataConfirm(LPHEAPBUF_MAN pBufMan, void *pBuf);

void TxqPri(u32 pri)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    LPTXQ pTxq = &pTxCtrl->Txq[pri];
    LPHEAPBUF_MAN pBufMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[pri];
    WlMaDataReq *pTxReq, *pNextTxReq;
    LPTXFRM pTxFrm;
    LPTXFRM_MAC pMacTxFrm;
    u16 *pMREG;
    u32 x, fc, cam_adrs, adrs;
    if (((*(LPHEAPBUF_MAN)pBufMan).Count) == 0) {
        ;
        return;
    }
    x = OS_DisableIrqMask((1UL << 24) );
    if (pTxq->Busy) {
        OS_EnableIrqMask(x);
        return;
    }
    pNextTxReq = (WlMaDataReq *)((u32)(*(LPHEAPBUF_MAN)pBufMan).Head) ;
next_TxqFrm:
    if ((u32)pNextTxReq == (u32)(-1) ) {
        OS_EnableIrqMask(x);
        return;
    }
    pTxReq = pNextTxReq;
    pNextTxReq = (WlMaDataReq *)GetHeapBufNextAdrs(pTxReq);
    pTxFrm = (LPTXFRM)&pTxReq->frame;
    cam_adrs = pTxFrm->FirmHeader.CamAdrs;
    if (CheckFrameTimeout(pTxFrm)) {
        pTxCtrl->TimeOutFrm++;
        pTxFrm->MacHeader.Tx.Status = 2;
        pTxq->OutCount++;
        (*pTxq->pEndFunc)(pTxFrm, 0 );
        goto next_TxqFrm;
    }
    if ((pri == 0) || ((pri == 1) && (CAM_GetStaState(cam_adrs) == 0x40 ))) {
        if (!CAM_IsActive(cam_adrs)) {
            goto next_TxqFrm;
        }
        if (CAM_GetStaState(cam_adrs) != 0x40 ) {
            ;
            pTxFrm->MacHeader.Tx.Status = 2;
            IssueMaDataConfirm(pBufMan, (void *)((u32)pTxFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
            CAM_DecFrameCount(pTxFrm);
            goto next_TxqFrm;
        }
    }
    pTxq->Busy = 1 ;
    pTxq->InCount++;
    pTxq->pFrm = pTxFrm;
