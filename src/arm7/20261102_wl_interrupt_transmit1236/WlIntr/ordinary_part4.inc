        }
        ;
        time[0] = *(vu16 *)((0x04808000) + 0x0F8) ;
        time[1] = *(vu16 *)((0x04808000) + 0x0FA) ;
        time[2] = *(vu16 *)((0x04808000) + 0x0F8) ;
        time[3] = *(vu16 *)((0x04808000) + 0x0FA) ;
        if (time[0] > time[2]) {
            time[0] = (time[2] >> 4) | (time[3] << 12);
        } else {
            time[0] = (time[0] >> 4) | (time[1] << 12);
        }
        ;
        if ((bnry >= (0x1000 + 0x1B0 - 36) / 2) && (bnry <= (0x1000 + 0x1DE ) / 2)) {
            WUpdateCounter();
        }
        pMFrm = (LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(bnry) * 2)) ;
        pStatus = (u16 *)pMFrm;
        pErrSts = (u16 *)((u32)pStatus + 2);
        pErrSts = (u16 *)AdjustRingPointer(pErrSts);
        pNextBnry = pErrSts;
        pTimeStamp = (u16 *)((u32)pErrSts + 2);
        pTimeStamp = (u16 *)AdjustRingPointer(pTimeStamp);
        pMPDU = (u16 *)((u32)pTimeStamp + 4);
        pMPDU = (u16 *)AdjustRingPointer(pMPDU);
        pDur = (u16 *)AdjustRingPointer(&pMFrm->Dot11Header.DurationID);
        *pStatus |= ((*pErrSts << 1) & (0x0001 << 10) );
        *pTimeStamp = (u16)time[0];
        length = *pMPDU;
        next_bnry = ((bnry * 2 + length + 3 + 12) / 4) * 2;
        if (next_bnry >= 0x1F60 / 2) {
            next_bnry -= pWork->Ofst.RxBuf.Size / 2;
        }
        if (length > (24 + 4 + 2312 + 4 + 4) ) {
            ;
            ;
            *pStatus = 0xFFFF;
            next_bnry = curr;
            pWork->CurrErrCount++;
            ;
        }
        else if (wlOperation & 0x00000001 ) {
            if (next_bnry != curr) {
                LPRXFRM_MAC pNextMFrm;
                u16 nextStatus, nextRate;
                pNextMFrm = (LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(next_bnry) * 2)) ;
                nextStatus = pNextMFrm->MacHeader.Rx.Status;
                if ((u32)pNextMFrm < ((0x04800000 + 0x4000) + 0x1F60 - 6)) {
                    nextRate = LoadLow(&pNextMFrm->MacHeader.Rx.Service_Rate);
                } else {
                    nextRate = *(u16 *)((u32)pNextMFrm - (u32)pWork->Ofst.RxBuf.Size + 6);
                }
                if ((nextStatus & 0x7C00) || ((nextRate != 0x0a ) && (nextRate != 0x14 )) || (length > 0x0FFF)) {
                    ;
                    pWork->CurrErrCount++;
                    *pStatus = 0xFFFF;
                    pRxCtrl->wlCurr = curr;
                    *pNextBnry = curr;
                    break;
                }
            }
        }
        frameType = *pStatus & (0x000F) ;
        if (frameType == (0x000C << 0) ) {
            u16 fc = *(u16 *)AdjustRingPointer(&pMFrm->Dot11Header.FrameCtrl.Data);
            u16 seqCtrl = *(u16 *)AdjustRingPointer(&pMFrm->Dot11Header.SeqCtrl.Data);
            if ((pRxCtrl->LastMpSeq == seqCtrl) && (fc & 0x0800 )) {
                ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.rx.mpDuplicateErr++;
                *pStatus = 0xFFFF;
            }
            else if ((((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.NullKeyRes == 0) && (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA == 0x40 )) {
                if ((*(vu16 *)((0x04808000) + 0x028) != 0) && (*(vu16 *)((0x04808000) + 0x098) & (0x0001 << 15) )) {
                    OS_CancelAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->KeyAlarm);
                    OS_SetAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->KeyAlarm, ((OSTick)(((33514000 / 1000) * (u64)(*pDur)) / 64 / 1000)) , WClearKSID, 0 );
                } else {
                    seqCtrl = 0xFFFF;
                    *(u16 *)((0x04800000 + 0x4000) + 0x1f7e) = 0xFFFF;
                    *(u16 *)((0x04808000) + 0x24C) = 0xFFFF;
                    *(u16 *)((0x04808000) + 0x24C + 2) = 0xFFFF;
                    *pStatus = 0xFFFF;
                }
            }
            pRxCtrl->LastMpSeq = seqCtrl;
            if (CheckKeyTxEnd() & 1) {
                ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.multiPoll.txNull++;
            }
        } else if (frameType == (0x000D << 0) ) {
            if ((((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.NullKeyRes == 0) && (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA == 0x40 )) {
                if ((*(vu16 *)((0x04808000) + 0x028) == 0) || ((*(vu16 *)((0x04808000) + 0x098) & (0x0001 << 15) ) == 0)) {
                    *pStatus = 0xFFFF;
                }
            }
        }
        pRxCtrl->wlCurr = next_bnry;
        *pNextBnry = next_bnry;
    }
    if (wlOperation & 0x00000001 ) {
        u16 bkcurr = *(vu16 *)((0x04808000) + 0x054) ;
        u16 v = (u16)CheckKeyTxEnd();
        if (v && (bkcurr == *(vu16 *)((0x04808000) + 0x054) )) {
            if (v & 2) {
                SetFatalErr(0x80);
            } else if (v & 1) {
                SetFatalErr(0x100);
            }
        }
    }
    if (*(vu16 *)((0x04808000) + 0x05A) != *(vu16 *)((0x04808000) + 0x054) ) {
        AddTask(0 , 15 );
    }
}
void WlIntrMpEnd(u32 bMacBugPatch)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u32 cnt;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 12) ;
    ;
    if (pTxCtrl->Mp.Busy == 0 ) {
        ;
        return;
    }
    ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000010 ) {
        if (bMacBugPatch) {
            u16 pri = *(vu16 *)((0x04808000) + 0x0B6) ;
            u16 state = *(vu16 *)(0x04808000 + 0x214) ;
            if ((state == 3 ) || (state == 5 )) {
                if (pri == 0) {
                    u16 tm, map;
                    ;
                    map = pTxCtrl->Mp.pMacFrm->MacHeader.Tx.Status2;
                    cnt = 0;
                    while (map != 0) {
                        cnt += (map & 1);
                        map >>= 1;
                    }
                    tm = cnt * (10 + *(u16 *)&pTxCtrl->Mp.pMacFrm->Body[0]) + 96 + (pTxCtrl->Mp.pMacFrm->MacHeader.Tx.MPDU) * 4 + 96;
                    SetupUsTimeOut(tm, MacBugTxMp);
                    ;
                    ;
                    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.MpEndErrCount++;
                    return;
                }
            }
        }
    }
    ;
    ;
    ;
    AddTask(0 , 16 );
    ;
}
void WlIntrStartTx(void) __attribute__((never_inline))
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u32 i, cnt;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 7) ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000020 ) {
        u16 sts = *(vu16 *)(0x04808000 + 0x214) & 0x00FF;
        u16 adr = *(vu16 *)((0x04808000) + 0x268) ;
        if (((sts >= 3) && (sts <= 5)) && ((adr >= ((u32)pTxCtrl->Key[0].pMacFrm / 2 & 0x0FFF)) && (adr <= ((u32)pTxCtrl->Txq[2].pMacFrm / 2 & 0x0FFF)))) {
            ;
            *(vu16 *)((0x04808000) + 0x244) |= 0x0080;
            *(vu16 *)((0x04808000) + 0x244) &= ~0x0080;
            ;
        }
    }
    if (*(vu16 *)((0x04808000) + 0x000) != 0x1440) {
        if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 6) | (0x0001 << 1) )) == ((0x0001 << 6) | (0x0001 << 1) )) {
            cnt = *(vu16 *)((0x04808000) + 0x2B8) ;
            if (cnt != 0) {
                i = 0;
                while (cnt == *(vu16 *)((0x04808000) + 0x2B8) ) {
                    if (i++ > 1000) {
                        ;
                        SetFatalErr(0x0040 );
                        break;
                    }
                }
            }
        }
    }
    ;
}
void WlIntrStartRx(void) __attribute__((never_inline))
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    *(vu16 *)((0x04808000) + 0x010) = (0x0001 << 6) ;
    ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000020 ) {
        if (pTxCtrl->BkKeyOut == 0xFFFF) {
            u32 i, tm;
            u16 *p;
            u16 curr, delt, duration, mpdu, tm_delt;
            ;
            if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) | (0x0001 << 1) )) != ((0x0001 << 0) | (0x0001 << 1) )) {
                goto not_suspend;
            }
            if (*(vu16 *)((0x04808000) + 0x268) < ((*(vu16 *)(0x04808000 + 0x050) / 2) & 0x0FFF)) {
                ;
                ;
                ;
                goto not_suspend;
            }
            curr = *(vu16 *)((0x04808000) + 0x054) ;
            {
                p = (u16 *)&((LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(curr) * 2)) )->MacHeader.Rx.MPDU;
                p = (u16 *)AdjustRingPointer(p);
                mpdu = *p;
                p += 2;
                p = (u16 *)AdjustRingPointer(p);
                if ((*p++ & 0xE7FF) == (((0x02 * 0x0004) | (0x02 * 0x0010)) | 0x0200) ) {
                    ;
                    ;
                    p = (u16 *)AdjustRingPointer(p);
                    tm = (u32) * (vu16 *)((0x04808000) + 0x0F8) - 0x10000UL;
                    while (1) {
                        delt = *(vu16 *)((0x04808000) + 0x268) - curr;
                        if (delt & 0x8000) {
                            delt += (pWork->Ofst.RxBuf.Size / 2);
                        }
                        if (delt > 6 + 1 + 1 + 3 + 3) {
                            break;
                        }
                        tm_delt = (u16)((u32) * (vu16 *)((0x04808000) + 0x0F8) - tm);
                        if (tm_delt > 16 * 4 ) {
                            goto not_suspend;
                        }
                    }
                    duration = *p;
                    p += 4;
                    for (i = 0; i < 3; i++) {
                        p = (u16 *)AdjustRingPointer(p);
                        if (*p++ != pWork->BSSID[i]) {
                            goto not_suspend;
                        }
                    }
                    p += 5;
                    p = (u16 *)AdjustRingPointer(p);
                    while (1) {
                        delt = *(vu16 *)((0x04808000) + 0x268) - curr;
                        if (delt & 0x8000) {
                            delt += (pWork->Ofst.RxBuf.Size / 2);
                        }
                        if (delt > 6 + 1 + 1 + 3 + 3 + 3 + 1 + 1 + 1) {
                            break;
                        }
                        tm_delt = (u16)((u32) * (vu16 *)((0x04808000) + 0x0F8) - tm);
                        if (tm_delt > 28 * 4 ) {
                            goto not_suspend;
                        }
                    }
                    if ((*p++ & (1UL << *(vu16 *)((0x04808000) + 0x028) )) == 0) {
                        ;
                        pTxCtrl->BkKeyOut = *(vu16 *)((0x04808000) + 0x098) ;
                        *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 6) ;
                        pWork->NotPollTxErrCount++;
                        while (1) {
                            if ((*(vu16 *)((0x04808000) + 0x19C) & ((0x0001 << 0) | (0x0001 << 1) )) != ((0x0001 << 0) | (0x0001 << 1) )) {
                                break;
                            }
                        }
                        *(vu16 *)((0x04808000) + 0x244) |= 0x0040;
                        *(vu16 *)((0x04808000) + 0x244) &= ~0x0040;
                        *(vu16 *)((0x04808000) + 0x228) = 0x0008;
                        *(vu16 *)((0x04808000) + 0x228) = 0x0000;
                        MultiPollRevicedClearSeq();
                    }
                }
            }
not_suspend:
            ;
        }
    }
    ;
    ;
}
void SetParentTbttTxq(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u32 bTask = 0 ;
    ResetTxqPri(2 );
    ResetTxqPri(1 );
    ResetTxqPri(0 );
    if (pTxCtrl->Txq[2 ].Busy) {
        if (pTxCtrl->Txq[2 ].pMacFrm->MacHeader.Tx.Status != 0) {
            bTask = 1 ;
        } else {
            pTxCtrl->Txq[2 ].Busy = 0;
        }
    }
    if (pTxCtrl->Txq[1 ].Busy) {
        if (pTxCtrl->Txq[1 ].pMacFrm->MacHeader.Tx.Status != 0) {
            bTask = 1 ;
        } else {
            pTxCtrl->Txq[1 ].Busy = 0;
        }
    }
    if (pTxCtrl->Txq[0 ].Busy) {
        if (pTxCtrl->Txq[0 ].pMacFrm->MacHeader.Tx.Status != 0) {
            bTask = 1 ;
        } else {
            pTxCtrl->Txq[0 ].Busy = 0;
        }
    }
    if (bTask) {
        AddTask(0 , 14 );
    }
    AddTask(0 , 20 );
}
void MacBugTxMp(void *arg)
{
    u32 x, i;
    u16 seqCtrl, seqCtrl2;
    x = OS_DisableIrqMask((1UL << 24) );
    seqCtrl = *(vu16 *)((0x04808000) + 0x210) ;
    *(vu16 *)((0x04808000) + 0x244) = 0x1000;
    for (i = 100; i > 0; i--) {
        seqCtrl2 = *(vu16 *)((0x04808000) + 0x210) ;
        if (seqCtrl != seqCtrl2) {
            break;
        }
    }
    *(vu16 *)((0x04808000) + 0x244) = 0x0000;
    WlIntrMpEnd(0 );
    OS_EnableIrqMask(x);
    ;
}
void *AdjustRingPointer(void *p)
{
    if ((u32)p >= ((0x04800000 + 0x4000) + 0x1F60 )) {
        p = (void *)((u32)p - (u32)((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Ofst.RxBuf.Size);
    }
    return p;
}
void MultiPollRevicedClearSeq(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    if (pTxCtrl->BkKeyOut != 0xFFFF) {
        u16 bkKeyIn;
        bkKeyIn = *(vu16 *)((0x04808000) + 0x094) ;
        *(vu16 *)((0x04808000) + 0x094) = pTxCtrl->BkKeyOut;
        *(vu16 *)((0x04808000) + 0x030) |= 0x0080;
        *(vu16 *)((0x04808000) + 0x094) = bkKeyIn;
        pTxCtrl->BkKeyOut = 0xFFFF;
        ;
    }
}
u32 CheckKeyTxEnd(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    return CheckKeyTxEndMain(&pTxCtrl->Key[0]) | CheckKeyTxEndMain(&pTxCtrl->Key[1]);
}
u32 CheckKeyTxEndMain(LPTXQ pTxq)
{
    u32 ret = 0;
    if (pTxq->Busy == 2) {
        if (((((u32)(pTxq->pMacFrm) & 0x3FFF) / 2) | (0x0001 << 15) ) != *(vu16 *)((0x04808000) + 0x094) ) {
            pTxq->Busy = 1;
            ret |= 1;
        }
    }
    if (pTxq->Busy == 1 && (pTxq->pMacFrm->MacHeader.Tx.Status & (0x0001 << 0) )) {
        TxEndKeyData(pTxq);
        ret |= 2;
    }
    return ret;
}
void InitializeIntr(void)
{
    OS_SetIrqFunction((1UL << 24) , WlIntr);
    OS_EnableIrqMask((1UL << 24) );
}
void ReleaseIntr(void)
{
    OS_DisableIrqMask((1UL << 24) );
    OS_SetIrqFunction((1UL << 24) , 0 );
}
