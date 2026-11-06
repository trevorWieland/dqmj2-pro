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
    pMacTxFrm = pTxq->pMacFrm;
    if (pWork->PowerState == ((0x0001 << 0) >> 1)) {
        WSetPowerState((0x0001 << 1) );
    }
    CopyTxFrmToMacBuf(pMacTxFrm, pTxReq);
    if (pWork->Mode == 1 ) {
        if (CAM_GetFrameCount(cam_adrs) > 1) {
            pMacTxFrm->Dot11Header.FrameCtrl.Data |= 0x2000 ;
        }
    }
    ;
    ;
    fc = pTxFrm->Dot11Header.FrameCtrl.Data;
    pMREG = (u16 *)(((0x04808000) + 0x0A0) + pri * 4);
    adrs = (u32)(((u32)(pMacTxFrm) & 0x3FFF) / 2) ;
    if ((fc & 0x000C ) == (0x01 * 0x0004 )) {
        *pMREG = (0x0001 << 15) | (0x0001 << 13) | (u16)adrs;
    } else if ((fc & (0x000C | 0x00F0 )) == ((0x00 * 0x0004) | (0x05 * 0x0010)) ) {
        *pMREG = (0x0001 << 15) | (0x0001 << 12) | (u16)adrs;
    } else {
        *pMREG = (0x0001 << 15) | (u16)adrs;
    }
    OS_EnableIrqMask(x);
}

void CopyTxFrmToMacBuf(LPTXFRM_MAC pMacTxFrm, WlMaDataReq *pTxReq)
{
    LPTXFRM pTxFrm = (LPTXFRM)&pTxReq->frame;
    if (pTxFrm->Dot11Header.FrameCtrl.Data & 0x4000 ) {
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode == 3 ) {
            WUpdateCounter();
        }
        if (pTxReq->header.code == 0xFFFF ) {
            DMA_WepWriteHeaderData(pMacTxFrm, &pTxFrm->MacHeader, pTxFrm->Data.Body, pTxFrm->FirmHeader.Length);
        } else {
            DMA_WepWriteHeaderData(pMacTxFrm, &pTxFrm->MacHeader, pTxFrm->Data.Pointer, pTxFrm->FirmHeader.Length);
        }
        *(vu16 *)&pMacTxFrm->Body[0] = *(vu16 *)(0x04808000 + 0x044) + (*(vu16 *)(0x04808000 + 0x044) << 8);
        *(vu16 *)&pMacTxFrm->Body[2] = (*(vu16 *)(0x04808000 + 0x044) & 0x00FF) | ((u32)((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.WepKeyId * (0x01 << 14) );
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000008 ) {
            u16 *pIcv = (u16 *)(((u32)&pMacTxFrm->Dot11Header + pTxFrm->MacHeader.Tx.MPDU - 8 + 1) & 0xFFFFFFFE);
            *pIcv++ = 0;
            *pIcv = 0;
        }
    } else {
        if (pTxReq->header.code == 0xFFFF ) {
            DMA_Write(pMacTxFrm, &pTxFrm->MacHeader, pTxFrm->FirmHeader.Length + sizeof(MAC_HEADER) + sizeof(DATA_HEADER));
        } else {
            DMA_WriteHeaderData(pMacTxFrm, &pTxFrm->MacHeader, pTxFrm->Data.Pointer, pTxFrm->FirmHeader.Length);
        }
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000004 ) {
        u16 *pId = (u16 *)(((u32)&pMacTxFrm->Dot11Header + pTxFrm->MacHeader.Tx.MPDU - 1) & 0xFFFFFFFC);
        *pId++ = 0xB6B8 ;
        *pId = 0x1D46 ;
    }
}

u32 CheckFrameTimeout(LPTXFRM pTxFrm)
{
    u16 delt, timeout;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    timeout = pWork->FrameLifeTime * 8;
    switch (pTxFrm->Dot11Header.FrameCtrl.Bit.Type) {
    case 0x00 :
        if (pWork->Mode == 1 ) {
            switch (pTxFrm->Dot11Header.FrameCtrl.Bit.SubType) {
            case 0x0B :
            case 0x01 :
            case 0x03 :
                timeout /= 8;
                break;
            }
        }
        break;
    default:
        timeout /= 8;
        break;
    }
    delt = pWork->IntervalCount - pTxFrm->FirmHeader.FrameTime;
    return delt > timeout;
}

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

void MakePsPollFrame(u16 aid)
{
    LPTXFRM_MAC pMFrm = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[2 ].pMacFrm;
    ;
    pMFrm->MacHeader.Tx.Status = 0;
    pMFrm->MacHeader.Tx.Status2 = 0;
    pMFrm->MacHeader.Tx.rsv_RetryCount = 0;
    pMFrm->MacHeader.Tx.MPDU = 28 - 6 - 2;
    pMFrm->Dot11Header.FrameCtrl.Data = ((0x01 * 0x0004) | (0x0A * 0x0010)) ;
    pMFrm->Dot11Header.DurationID = 0xC000 | aid;
    WSetMacAdrs2(pMFrm->Dot11Header.Adrs1, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MacAdrs);
}

void InitManHeader(LPTXFRM pFrm, u16 *pDA)
{
    MI_CpuClear16(pFrm, (sizeof(FIRM_HEADER) + sizeof(MAC_HEADER) + sizeof(MAN_HEADER)) );
    pFrm->MacHeader.Tx.Service_Rate = WCalcManRate();
    WSetMacAdrs3(pFrm->Dot11Header.Adrs1, pDA, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MacAdrs, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID);
}

u32 IsExistManFrame(u16 *pDA, u16 frameCtrl)
{
    WlMaDataReq *pReq;
    LPTXFRM pFrm;
    pReq = (WlMaDataReq *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[1]).Head) ;
    while ((u32)pReq != (u32)(-1) ) {
        pFrm = (LPTXFRM)&pReq->frame;
        if ((pFrm->Dot11Header.FrameCtrl.Data == frameCtrl) && MatchMacAdrs(pFrm->Dot11Header.Adrs1, pDA)) {
            ;
            return 1 ;
        }
        pReq = (WlMaDataReq *)GetHeapBufNextAdrs(pReq);
    }
    return 0 ;
}
