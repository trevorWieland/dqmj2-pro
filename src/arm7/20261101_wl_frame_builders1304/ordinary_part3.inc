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

void WClearKSID(void *arg);

void WSetMacAdrs1(u16 *dst, u16 *src1);

void WSetMacAdrs2(u16 *dst, u16 *src1, u16 *src2);

void WSetMacAdrs3(u16 *dst, u16 *src1, u16 *src2, u16 *src3);

u32 MatchMacAdrs(u16 *pAdrs1, u16 *pAdrs2);

u32 WCalcManRate(void);

void WL_WriteByte(void *p, u8 data);

u8 WL_ReadByte(void *p);

void SetFatalErr(u32 errCode);

extern const u16 RateBit2Element[];

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

void ClearTxKeyData(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u32 x;
    x = OS_DisableIrqMask((1UL << 24) );
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.NullKeyRes == 0) {
        WClearKSID(0 );
    }
    *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 7) | (0x0001 << 6) ;
    pTxCtrl->Key[0].Busy = 0 ;
    pTxCtrl->Key[1].Busy = 0 ;
    OS_EnableIrqMask(x);
}

void ClearQueuedPri(u32 pri)
{
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[pri];
    if (!pTxq->Busy) {
        return;
    }
    if (pTxq->pMacFrm->MacHeader.Tx.Status == 0) {
        pTxq->pFrm->MacHeader.Tx.Status = 2;
    } else {
        pTxq->pFrm->MacHeader.Tx.Status = pTxq->pMacFrm->MacHeader.Tx.Status;
    }
    (*pTxq->pEndFunc)(pTxq->pFrm, 0 );
}

static const u16 Pri2QBit[] = { 0x01, 0x04, 0x08 };

void ResetTxqPri(u32 pri)
{
    u32 x;
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[pri];
    x = OS_DisableIrqMask((1UL << 24) );
    *(vu16 *)((0x04808000) + 0x0B4) = Pri2QBit[pri];
    if (pTxq->Busy) {
        if ((pTxq->pFrm->Dot11Header.FrameCtrl.Data & 0x4000 ) == 0) {
            pTxq->pFrm->MacHeader.Tx.rsv_RetryCount = pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount;
        }
        pTxq->pFrm->Dot11Header.SeqCtrl.Data = pTxq->pMacFrm->Dot11Header.SeqCtrl.Data;
        ;
        ;
    }
    OS_EnableIrqMask(x);
}

void DeleteAllTxFrames(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    switch (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode) {
    case 1 :
        MessageDeleteTx(0, 1 );
        MessageDeleteTx(1, 0 );
        MessageDeleteTx(2, 1 );
        if (pTxCtrl->Mp.Busy) {
            ;
            pTxCtrl->Mp.Busy = 0;
            pTxCtrl->Mp.InCount--;
            ReleaseHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pTxCtrl->pMpEndInd);
        }
        break;
    case 2 :
    case 3 :
        MessageDeleteTx(0, 1 );
        MessageDeleteTx(1, 0 );
        MessageDeleteTx(2, 0 );
        break;
    default:
        MessageDeleteTx(0, 0 );
        MessageDeleteTx(1, 0 );
        MessageDeleteTx(2, 0 );
        break;
    }
}

void MessageDeleteTx(u32 pri, u32 bMsg)
{
    WlMaDataReq *pReq, *pNextReq;
    LPTXFRM pFrm;
    pReq = (WlMaDataReq *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[pri]).Head) ;
    if ((u32)pReq == (u32)(-1) ) {
        return;
    }
    do {
        pNextReq = (WlMaDataReq *)GetHeapBufNextAdrs(pReq);
        pFrm = (LPTXFRM)&pReq->frame;
        if (pri != 2 ) {
            CAM_DecFrameCount(pFrm);
        }
        pFrm->MacHeader.Tx.Status = 2;
        if (bMsg) {
            IssueMaDataConfirm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[pri], pReq);
        }
        pReq = pNextReq;
    } while ((u32)pReq != (u32)(-1) );
}

void TxPsPollFrame(void)
{
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[2 ];
    pTxq->InCount++;
    ;
    if (pTxq->Busy) {
        pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount = 0;
    } else {
        pTxq->Busy = 1 ;
        pTxq->pMacFrm->MacHeader.Tx.Status = 0;
        pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount = 0;
        pTxq->pMacFrm->MacHeader.Tx.Service_Rate = WCalcManRate();
        *(vu16 *)(((0x04808000) + 0x0A0) + 2 * 4) = (0x0001 << 15) | (u16)(((u32)(pTxq->pMacFrm) & 0x3FFF) / 2) ;
    }
}

void StartBeaconFrame(void)
{
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon;
    pTxq->Busy = 1 ;
    *(vu16 *)((0x04808000) + 0x080) = (0x0001 << 15) | (((u32)(pTxq->pMacFrm) & 0x3FFF) / 2) ;
}

void StopBeaconFrame(void)
{
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon;
    *(vu16 *)((0x04808000) + 0x080) = 0;
    pTxq->Busy = 0 ;
}

u32 IsEnableManagement(void)
{
    if (((*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[1]).Count) < (24 - ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.ConnectSta)) {
        return 1 ;
    }
    ;
    return 0 ;
}

LPDISASS_FRAME MakeDisAssFrame(u16 *pDA, u16 reasonCode)
{
    WlMaDataReq *pReq;
    LPDISASS_FRAME pFrm;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(DISASS_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPDISASS_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPDISASS_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.ReasonCode = reasonCode;
    pFrm->FirmHeader.Length = 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x0A * 0x0010)) ;
    return pFrm;
}

LPASSREQ_FRAME MakeAssReqFrame(u16 *pDA)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaDataReq *pReq;
    LPASSREQ_FRAME pFrm;
    u32 ofst;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(ASSREQ_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPASSREQ_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPASSREQ_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.CapaInfo.Data = pWork->CapaInfo;
    pFrm->Body.ListenInterval = pWork->ListenInterval;
    ofst = SetSSIDElement(&pFrm->Body.Buf[0]);
    ofst += SetSupRateSet(&pFrm->Body.Buf[ofst]);
    pFrm->FirmHeader.Length = ofst + 2 + 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x00 * 0x0010)) ;
    return pFrm;
}

LPREASSREQ_FRAME MakeReAssReqFrame(u16 *pDA)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaDataReq *pReq;
    LPREASSREQ_FRAME pFrm;
    u32 ofst;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(REASSREQ_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPREASSREQ_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPREASSREQ_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.CapaInfo.Data = pWork->CapaInfo;
    pFrm->Body.ListenInterval = pWork->ListenInterval;
    WSetMacAdrs1(pFrm->Body.CurrAPMacAdrs, pWork->LinkAdrs);
    ofst = SetSSIDElement(&pFrm->Body.Buf[0]);
    ofst += SetSupRateSet(&pFrm->Body.Buf[ofst]);
    pFrm->FirmHeader.Length = ofst + 2 + 2 + 6;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x02 * 0x0010)) ;
    return pFrm;
}
