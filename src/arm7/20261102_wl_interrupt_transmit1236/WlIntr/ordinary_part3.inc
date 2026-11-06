void *AdjustRingPointer(void *p);
void WlIntrPreTbtt(void) __attribute__((never_inline));
void WlIntrTbtt(void) __attribute__((never_inline));
void WlIntrActEnd(void) __attribute__((never_inline));
void WlIntrRfWakeup(void) __attribute__((never_inline));
void WlIntrCntOvf(void) __attribute__((never_inline));
void WlIntrTxErr(void) __attribute__((never_inline));
void WlIntrRxCntup(void) __attribute__((never_inline));
void WlIntrTxEnd(void) __attribute__((never_inline));
void WlIntrRxEnd(void) __attribute__((never_inline));
void WlIntrMpEnd(u32 bMacBugPatch);
void WlIntrStartTx(void) __attribute__((never_inline));
void WlIntrStartRx(void) __attribute__((never_inline));
void SetParentTbttTxq(void);
void MacBugTxMp(void *arg);
void MultiPollRevicedClearSeq(void);
u32 CheckKeyTxEnd(void);
u32 CheckKeyTxEndMain(LPTXQ pTxq);
void WlIntr(void)
{
    u32 isr;
    while (1) {
        isr = *(vu16 *)((0x04808000) + 0x010) & *(vu16 *)((0x04808000) + 0x012) ;
        if (isr == 0) {
            break;
        }
        if (isr & (0x0001 << 7) ) {
            WlIntrStartTx();
        }
        if (isr & (0x0001 << 6) ) {
            WlIntrStartRx();
        }
        if (isr & (0x0001 << 15) ) {
            WlIntrPreTbtt();
        }
        if (isr & (0x0001 << 14) ) {
            WlIntrTbtt();
        }
        if (isr & (0x0001 << 13) ) {
            WlIntrActEnd();
        }
        if (isr & (0x0001 << 11) ) {
            WlIntrRfWakeup();
        }
        if (isr & (0x0001 << 3) ) {
            WlIntrTxErr();
        }
        if (isr & (0x0001 << 2) ) {
            WlIntrRxCntup();
        }
        if (isr & (0x0001 << 0) ) {
            WlIntrRxEnd();
        }
        if (isr & (0x0003 << 4) ) {
            WlIntrCntOvf();
        }
        if (isr & (0x0001 << 1) ) {
            WlIntrTxEnd();
        }
        if (isr & (0x0001 << 12) ) {
            WlIntrMpEnd(1);
        }
    }
    ;
    OS_SetIrqCheckFlag((1UL << 24) );
}
void WlIntrPreTbtt(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 15) ;
    ;
    ;
    if ((pWork->STA == 0x40 ) && (pWork->BeaconLostTh != 0) && (pWork->CurrListenInterval == pWork->ListenInterval)) {
        if (++pWork->BeaconLostCnt > pWork->BeaconLostTh) {
            ;
            ;
            pWork->BeaconLostCnt = 0;
            AddTask(1 , 13 );
            ;
            ;
        }
    }
    pWork->PowerState = 1;
    ;
}
void WlIntrTbtt(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u8 *p;
    u32 txq, i, vtsf;
    u32 bWakeUp;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 14) ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
    switch (pWork->Mode) {
    case 1 :
        p = (u8 *)((u32)pTxCtrl->Beacon.pMacFrm->Body + pWork->Ofst.Beacon.GameInfo + 2 + 3 + 1 + 2);
        vtsf = *(vu16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) ;
        WL_WriteByte(p++, vtsf & 0x00FF);
        WL_WriteByte(p, vtsf >> 8);
        if (pWork->PowerMgtMode == 1 ) {
            *(vu16 *)((0x04808000) + 0x134) = (u32)pConfig->ActiveZone + *(vu16 *)((0x04808000) + 0x134) + 1;
        }
        { ((LPWL_MAN)native_host_arm7_data_0380fff4)->CamMan.PowerState = (~((LPWL_MAN)native_host_arm7_data_0380fff4)->CamMan.PowerMgtMode) | ((LPWL_MAN)native_host_arm7_data_0380fff4)->CamMan.NotClass3; } ;
        txq = *(vu16 *)((0x04808000) + 0x0B6) ;
        if ((txq & ((0x0001 << 4) | (0x0001 << 3) )) || ((txq & ((0x0001 << 2) | (0x0001 << 1) )) == (0x0001 << 1) )) {
            pTxCtrl->Flag &= ~0x0002 ;
            SetParentTbttTxq();
        } else {
            pTxCtrl->Flag |= 0x0002 ;
        }
        break;
    case 2 :
        if (pWork->bSynchro) {
            *(vu16 *)((0x04808000) + 0x134) = (u32)pConfig->ActiveZone + *(vu16 *)((0x04808000) + 0x134) + 1;
        } else {
            *(vu16 *)((0x04808000) + 0x134) = 0xFFFF;
        }
        if (pWork->bFirstTbtt == 2) {
            WSetPowerState((0x0001 << 1) );
        }
    case 3 :
        if (pWork->STA != 0x40 ) {
            bWakeUp = 1 ;
        } else {
            bWakeUp = 0 ;
            if (pWork->CurrListenInterval == 1) {
                bWakeUp = 1 ;
            }
            if (pWork->RxDtims) {
                if ((pWork->DTIMCount == 1) || ((pWork->DTIMCount == 0) && (pWork->DTIMPeriod == 1))) {
                    bWakeUp = 1 ;
                }
            }
        }
        if (bWakeUp) {
            ;
            *(vu16 *)((0x04808000) + 0x038) |= (0x0001 << 0) ;
            ;
        } else {
            ;
            *(vu16 *)((0x04808000) + 0x038) &= ~(0x0001 << 0) ;
            ;
        }
        if (*(vu16 *)((0x04808000) + 0x118) > 10) {
            *(vu16 *)((0x04808000) + 0x048) = 0;
        }
        if (--pWork->CurrListenInterval == 0) {
            pWork->CurrListenInterval = pWork->ListenInterval;
        }
        if (pWork->DTIMCount-- == 0) {
            pWork->DTIMCount = pWork->DTIMPeriod - 1;
        }
        for (i = 0; i < 2; i++) {
            LPTXQ pTxq = &pTxCtrl->Txq[i];
            if (pTxq->Busy && (pTxq->pFrm->MacHeader.Tx.Status == 0)) {
                if (CheckFrameTimeout(pTxq->pFrm)) {
                    ResetTxqPri(i);
                    ;
                    pTxq->pMacFrm->MacHeader.Tx.Status = 2;
                    AddTask(0 , 14 );
                    pTxCtrl->TimeOutFrm++;
                }
            }
        }
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 3) | (0x0001 << 2) | (0x0001 << 0) ;
        break;
    }
    ;
    ;
}
void WlIntrActEnd(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 13) ;
    *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 3) | (0x0001 << 2) | (0x0001 << 0) ;
    if (pWork->bFirstTbtt == 1) {
        pWork->bFirstTbtt = 2;
    } else if (pWork->bFirstTbtt == 2) {
        pWork->bFirstTbtt = 0;
    } else if ((pWork->Mode == 2 ) && (pWork->STA != 0x40 )) {
        *(vu16 *)((0x04808000) + 0x048) = 0;
    }
}
void WlIntrRfWakeup(void) __attribute__((never_inline))
{
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 11) ;
    ;
    ;
    ;
    ;
    ;
    ;
    ;
}
void WlIntrCntOvf(void) __attribute__((never_inline))
{
    ;
    ;
    WUpdateCounter();
    ;
    *(vu16 *)((0x04808000) + 0x1AC) = 0xFFFF;
    *(vu16 *)((0x04808000) + 0x010) = (0x0003 << 4) ;
}
void WlIntrTxErr(void) __attribute__((never_inline))
{
    LPTXFRM_MAC pMFrm;
    u32 i;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 3) ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Diversity != 0 ) {
        if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) || (0x0001 << 6) )) == 0) {
            *(vu16 *)(0x04808000 + 0x290) ^= 1 ;
        }
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000008 ) {
        LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
        LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
        for (i = 0; i < 3; i++) {
            if (pTxCtrl->Txq[i].Busy) {
                pMFrm = (LPTXFRM_MAC)pTxCtrl->Txq[i].pMacFrm;
                if ((pMFrm->Dot11Header.FrameCtrl.Data & 0x4000 ) && (LoadLow(&pMFrm->MacHeader.Tx.rsv_RetryCount) != 0)) {
                    u16 *pIcv = (u16 *)(((u32)&pMFrm->Dot11Header + pMFrm->MacHeader.Tx.MPDU - 8 + 1) & 0xFFFFFFFE);
                    if ((pIcv[0] == 0) && (pIcv[1] == 0)) {
                        pMFrm->MacHeader.Tx.rsv_RetryCount = 0;
                        *(vu16 *)((0x04808000) + 0x032) = 0x0000;
                        *(vu16 *)((0x04808000) + 0x032) = 0x8000;
                        pWork->WepErrCount++;
                        ;
                        ;
                        ;
                    }
                }
            }
        }
    }
    ;
}
void WlIntrRxCntup(void) __attribute__((never_inline))
{
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl;
    LPTXQ pTxq = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq;
    u32 isr;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 2) ;
    isr = *(vu16 *)((0x04808000) + 0x1A8) ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000008 ) {
        if (isr & (0x0001 << 10) ) {
            u16 map;
            ;
            map = *(vu16 *)((0x04808000) + 0x0B0) ;
            if ((((map & (0x0001 << 0) ) == 0) || (pTxq[0].Busy == 0)) && (((map & (0x0001 << 2) ) == 0) || (pTxq[1].Busy == 0)) && (((map & (0x0001 << 3) ) == 0) || (pTxq[2].Busy == 0)) && ((*(vu16 *)((0x04808000) + 0x19C) & (0x0001 << 0) ) == 0)) {
                *(vu16 *)((0x04808000) + 0x032) = 0x0000;
                *(vu16 *)((0x04808000) + 0x032) = 0x8000;
                pRxCtrl->IcvOkCntFlag = 0;
            }
            else if (pRxCtrl->IcvOkCntFlag++ > 12) {
                ;
                pRxCtrl->IcvOkCntFlag = 0;
                *(vu16 *)((0x04808000) + 0x032) = 0x0000;
                *(vu16 *)((0x04808000) + 0x032) = 0x8000;
                ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.WepErrCount++;
                ;
            }
        }
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000001 ) {
        if (isr & ((0x0001 << 5) | (0x0001 << 6) )) {
            u16 curr = *(vu16 *)((0x04808000) + 0x054) ;
            if ((curr >= (*(vu16 *)(0x04808000 + 0x052) - ((0x04800000 + 0x4000) & 0xFFFF)) / 2) || (curr < (*(vu16 *)(0x04808000 + 0x050) - ((0x04800000 + 0x4000) & 0xFFFF)) / 2)) {
                *(vu16 *)((0x04808000) + 0x056) = *(vu16 *)((0x04808000) + 0x05A) ;
                *(u16 *)((0x04808000) + 0x030) = 0x8001;
                ;
                ;
                ;
            }
            WCheckTxBuf();
        }
    }
}
void WlIntrTxEnd(void) __attribute__((never_inline))
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u32 txFrm;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 1) ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA == 0x12 ) {
        void IntrCarrierSuppresionSignal(void);
        IntrCarrierSuppresionSignal();
        return;
    }
    ;
    ;
    txFrm = *(vu16 *)((0x04808000) + 0x0B8) & (0x000F << 8) ;
    switch (txFrm) {
    case (0x0003 << 8) :
        if (pTxCtrl->Flag & 0x0002 ) {
            SetParentTbttTxq();
        }
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.tx.beacon++;
        AddTask(0 , 8 );
        break;
    case (0x0008 << 8) :
        ;
        if (pTxCtrl->RetryLimit <= (u16)LoadLow(&pTxCtrl->Mp.pMacFrm->MacHeader.Tx.rsv_RetryCount)) {
            *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 1) ;
            pTxCtrl->MpBlkCnt++;
            ;
        }
        pTxCtrl->pMpEndInd->mpKey.txCount++;
        break;
    case (0x000B << 8) :
        ;
        *(u16 *)((0x04800000 + 0x4000) + 0x1f70) = 0xFFFF;
        *(u16 *)((0x04800000 + 0x4000) + 0x1f72) = 0xFFFF;
        *(u16 *)((0x04808000) + 0x24C) = 0xFFFF;
        *(u16 *)((0x04808000) + 0x24C + 2) = 0xFFFF;
        if (pTxCtrl->Mp.Busy) {
            if (pTxCtrl->Mp.pMacFrm->Dot11Header.SeqCtrl.Data == 0xFFFF) {
                u16 retry = pTxCtrl->Mp.pMacFrm->MacHeader.Tx.rsv_RetryCount;
                if (retry != 0) {
                    pTxCtrl->Mp.pMacFrm->MacHeader.Tx.rsv_RetryCount = 0;
                    ;
                    pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2 = pTxCtrl->SetKeyMap;
                }
            }
        }
        {
            u16 setmap, pollmap;
            WlMpKeyData *pKeyData;
            setmap = pTxCtrl->SetKeyMap;
            pollmap = pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2;
            pKeyData = (WlMpKeyData *)pTxCtrl->pMpEndInd->mpKey.data;
            if ((pollmap > 1) && (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Diversity != 0 )) {
                if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) || (0x0001 << 6) )) == 0) {
                    *(vu16 *)(0x04808000 + 0x290) ^= 1 ;
                }
            }
            if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000040 ) {
                while (pollmap > 1) {
                    pollmap >>= 1;
                    if (pollmap & 1) {
                        pKeyData->noResponse++;
                    }
                    setmap >>= 1;
                    if (setmap & 1) {
                        pKeyData = (WlMpKeyData *)((u32)pKeyData + pTxCtrl->pMpEndInd->mpKey.length);
                    }
                }
            }
        }
        break;
    default:
        break;
    }
    if ((txFrm != (0x0008 << 8) ) && ((*(vu16 *)((0x04808000) + 0x0B0) & (0x0001 << 1) ) == 0)) {
        if (pTxCtrl->Mp.Busy) {
            *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 1) ;
            *(vu16 *)((0x04808000) + 0x048) = 0;
            if ((*(vu16 *)((0x04808000) + 0x010) & (0x0001 << 12) ) == 0) {
                WlIntrMpEnd(2);
            } else {
                pTxCtrl->MpLastOk++;
            }
            pTxCtrl->MpRstCnt++;
        }
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 1) ;
        ;
    }
    AddTask(0 , 14 );
    ;
}
void WlIntrRxEnd(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl;
    LPRXFRM_MAC pMFrm;
    u32 wlOperation = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation;
    u16 *pStatus, *pErrSts, *pNextBnry, *pTimeStamp, *pMPDU, *pDur;
    u32 bnry, curr, next_bnry, length, time[4], frameType;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 0) ;
    ;
    ;
    if (pWork->Mode == 0 ) {
        *(vu16 *)((0x04808000) + 0x05A) = *(vu16 *)((0x04808000) + 0x054) ;
    }
    for (;;) {
        bnry = pRxCtrl->wlCurr;
        curr = *(vu16 *)((0x04808000) + 0x054) ;
        if (bnry == curr) {
            break;
