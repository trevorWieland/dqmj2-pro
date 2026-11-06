void TxqEndData(LPTXFRM pFrm, u32 flag)
{
    LPHEAPBUF_MAN pBufMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[0 ];
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    void *pReq = (void *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    CAM_DecFrameCount(pFrm);
    if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
        pCounter->tx.success++;
        if (pFrm->Dot11Header.FrameCtrl.Bit.ToDS) {
            if (pFrm->Dot11Header.Adrs3[0] & 0x0001) {
                pCounter->tx.multicast++;
            } else {
                pCounter->tx.unicast++;
            }
        } else {
            if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                pCounter->tx.multicast++;
            } else {
                pCounter->tx.unicast++;
            }
        }
    } else {
        pCounter->tx.failed++;
    }
    if (pFrm->Dot11Header.FrameCtrl.Bit.WEP) {
        pCounter->tx.wep++;
    }

    IssueMaDataConfirm(pBufMan, pReq);
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[0 ].Busy = 0 ;
    if (CAM_GetPowerMgtMode(pFrm->FirmHeader.CamAdrs)) {
        if ((pFrm->Dot11Header.FrameCtrl.Data & 0x2000 ) == 0) {
            CAM_SetDoze(pFrm->FirmHeader.CamAdrs);
        }
    }
    if (flag) {
        if (((*(LPHEAPBUF_MAN)pBufMan).Count) ) {
            TxqPri(0 );
        } else if ((pWork->Mode == 2 ) || (pWork->Mode == 3 )) {
            if ((pWork->STA == 0x40 ) && (pWork->PowerMgtMode) && (CAM_GetFrameCount(pWork->APCamAdrs) == 0) && (pWork->bExistTIM == 0x00 )) {
                WSetPowerState((0x0001 << 0) );
            }
        }
    }
}
void TxqEndManCtrl(LPTXFRM pFrm, u32 flag)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    LPHEAPBUF_MAN pBufMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[1 ];
    LPAUTH_FRAME pAuth;
    LPASSRES_FRAME pAssRes;
    LPDISASS_FRAME pDisAss;
    LPDEAUTH_FRAME pDeAuth;
    u32 bRelease = 1 ;
    u32 i, type, cam_adrs;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
        pCounter->tx.success++;
        if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
            pCounter->tx.multicast++;
        } else {
            pCounter->tx.unicast++;
        }
        if (CAM_GetPowerMgtMode(cam_adrs)) {
            if ((pFrm->Dot11Header.FrameCtrl.Data & 0x2000 ) == 0) {
                CAM_SetDoze(cam_adrs);
            }
        }
    } else {
        pCounter->tx.failed++;
    }
    if (pFrm->Dot11Header.FrameCtrl.Bit.WEP) {
        pCounter->tx.wep++;
    }
    pCounter->tx.retry += LoadLow(&pFrm->MacHeader.Tx.rsv_RetryCount);
    type = pFrm->Dot11Header.FrameCtrl.Data & (0x00F0 | 0x000C );
    switch (type) {
    case ((0x00 * 0x0004) | (0x0B * 0x0010)) :
        if (cam_adrs == 0) {
            break;
        }
        if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
            pAuth = (LPAUTH_FRAME)pFrm;
            if ((pAuth->Body.AlgoType == 0 ) && (pAuth->Body.SeqNum == 2) && (pAuth->Body.StatusCode == 0 )) {
                CAM_SetStaState(cam_adrs, 0x30 );
                MLME_IssueAuthIndication(pAuth->Dot11Header.DA, pAuth->Body.AlgoType);
            } else if ((pAuth->Body.AlgoType == 1 ) && (pAuth->Body.SeqNum == 4) && (pAuth->Body.StatusCode == 0 )) {
                CAM_SetStaState(cam_adrs, 0x30 );
                MLME_IssueAuthIndication(pAuth->Dot11Header.DA, pAuth->Body.AlgoType);
            }
        }
        else {
        }
        break;
    case ((0x00 * 0x0004) | (0x01 * 0x0010)) :
    case ((0x00 * 0x0004) | (0x03 * 0x0010)) :
        if (cam_adrs == 0) {
            break;
        }
        pAssRes = (LPASSRES_FRAME)pFrm;
        if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
            if ((pAssRes->Body.StatusCode == 0 ) && (CAM_GetStaState(cam_adrs) == 0x30 )) {
                CAM_SetStaState(cam_adrs, 0x40 );
                if (type == ((0x00 * 0x0004) | (0x01 * 0x0010)) ) {
                    MLME_IssueAssIndication(pAssRes->Dot11Header.DA, pAssRes->Body.AID, (LPSSID_ELEMENT)((u32)&pFrm->Dot11Header + pFrm->MacHeader.Tx.MPDU));
                } else {
                    MLME_IssueReAssIndication(pAssRes->Dot11Header.DA, pAssRes->Body.AID, (LPSSID_ELEMENT)((u32)&pFrm->Dot11Header + pFrm->MacHeader.Tx.MPDU));
                }
            }
        }
        else {
            CAM_ReleaseAID(cam_adrs);
            pDeAuth = MakeDeAuthFrame(pAssRes->Dot11Header.DA, 1 , 0 );
            if ((u32)pDeAuth != (0) ) {
                pDeAuth->FirmHeader.FrameId = 0x0002 ;
                if (flag) {
                    TxManCtrlFrame((LPTXFRM)pDeAuth);
                } else {
                    SetManCtrlFrame((LPTXFRM)pDeAuth);
                }
            }
        }
        break;
    case ((0x00 * 0x0004) | (0x0A * 0x0010)) :
        if (pWork->Mode == 1 ) {
            if (cam_adrs != 0) {
                if (CAM_GetStaState(cam_adrs) > 0x30 ) {
                    CAM_SetStaState(cam_adrs, 0x30 );
                }
            } else if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                for (i = 1; i < ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum; i++) {
                    if (CAM_GetStaState(i) > 0x30 ) {
                        CAM_SetStaState(i, 0x30 );
                    }
                }
            }
        } else {
            if (pWork->STA > 0x30 ) {
                WSetStaState(0x30 );
                WClearAids();
            }
        }
        if ((pMLME->State == (0x01 | 0x70) ) && (pFrm == pMLME->Work.DisAss.pTxFrm)) {
            pDisAss = (LPDISASS_FRAME)pFrm;
            if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
                pMLME->pCfm.DisAss->resultCode = 0x00 ;
            } else {
                pMLME->pCfm.DisAss->resultCode = 0x0C ;
            }
            pMLME->State = 0x00 ;
            IssueMlmeConfirm();
        }
        break;
    case ((0x00 * 0x0004) | (0x0C * 0x0010)) :
        if (pWork->Mode == 1 ) {
            if (cam_adrs != 0) {
                if (CAM_GetStaState(cam_adrs) > 0x20 ) {
                    CAM_SetStaState(cam_adrs, 0x20 );
                }
            } else if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                for (i = 1; i < ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum; i++) {
                    if (CAM_GetStaState(i) > 0x20 ) {
                        CAM_SetStaState(i, 0x20 );
                    }
                }
            }
        } else {
            if (pWork->STA > 0x20 ) {
                WSetStaState(0x20 );
                WClearAids();
            }
        }
        if ((pMLME->State == (0x01 | 0x40) ) && (pFrm == pMLME->Work.DeAuth.pTxFrm)) {
            pDeAuth = (LPDEAUTH_FRAME)pFrm;
            if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
                pMLME->pCfm.DeAuth->resultCode = 0x00 ;
            } else {
                pMLME->pCfm.DeAuth->resultCode = 0x0C ;
            }
            pMLME->State = 0x00 ;
            IssueMlmeConfirm();
        }
        if (pFrm->FirmHeader.FrameId == 0x0001 ) {
            ;
            if (cam_adrs != 0) {
                ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotSetTIM &= ~(1 << cam_adrs);
                CAM_Delete(cam_adrs);
            }
            MLME_IssueDeAuthIndication(pFrm->Dot11Header.Adrs1, 1 );
        } else if (pFrm->FirmHeader.FrameId == 0x0002 ) {
            ;
            pDeAuth = (LPDEAUTH_FRAME)pFrm;
            MLME_IssueDeAuthIndication(pFrm->Dot11Header.Adrs1, pDeAuth->Body.ReasonCode);
        }
        break;
    default:
        break;
    }
    if (bRelease) {
        CAM_DecFrameCount(pFrm);
        ReleaseHeapBuf(pBufMan, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[1 ].Busy = 0 ;
    if (flag && ((*(LPHEAPBUF_MAN)pBufMan).Count) ) {
        TxqPri(1 );
    }
}
void TxqEndPsPoll(LPTXFRM pFrm, u32 flag)
{
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    LPTXFRM_MAC pMFrm = (LPTXFRM_MAC)pFrm;
    pCounter->tx.retry += LoadLow(&pMFrm->MacHeader.Tx.rsv_RetryCount);
    if ((pMFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
        pCounter->tx.success++;
        pCounter->tx.unicast++;
    } else {
        pCounter->tx.failed++;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[2 ].Busy = 0 ;
    ;
}
void TxqEndBroadCast(LPTXFRM pFrm, u32 flag)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    LPHEAPBUF_MAN pBufMan = &pHeapMan->TxPri[2 ];
    LPTXFRM_MAC pMacFrm;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.tx.multicast++;
    if (pFrm->Dot11Header.FrameCtrl.Bit.Type == 0) {
        CAM_IncFrameCount(pFrm);
        MoveHeapBuf(pBufMan, &pHeapMan->TxPri[1 ], (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
        TxqEndManCtrl(pFrm, 0 );
    } else {
        IssueMaDataConfirm(pBufMan, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[2 ].Busy = 0 ;
    pMacFrm = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[2 ].pMacFrm;
    if (pMacFrm->Dot11Header.FrameCtrl.Bit.MoreData == 0) {
        *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 3) ;
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 2) | (0x0001 << 0) ;
        if (flag) {
            if (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[1]).Count) != 0) {
                TxqPri(1 );
            }
            if (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[0]).Count) != 0) {
                TxqPri(0 );
            }
        }
    }
    if (((*(LPHEAPBUF_MAN)pBufMan).Count) ) {
        if (flag) {
            TxqPri(2 );
        }
    } else {
        CAM_ClrTIMElementBitmap(0);
    }
}
void TxEndKeyData(LPTXQ pTxq)
{
    u32 retrycnt = LoadLow(&pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount);
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    if (retrycnt == 0) {
        ;
        pCounter->multiPoll.txNull++;
    } else {
        ;
        pCounter->multiPoll.txKey += retrycnt;
    }
    pTxq->OutCount++;
    pTxq->Busy = 0 ;
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
void ClearTxMp(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u32 x;
    x = OS_DisableIrqMask((1UL << 24) );
    *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 1) ;
    if (pTxCtrl->Mp.Busy) {
        WlIntrMpEndTask();
    }
    OS_EnableIrqMask(x);
}
void ClearTxData(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    u32 x;
    x = OS_DisableIrqMask((1UL << 24) );
    switch (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode) {
    case 1 :
        *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 0) | (0x0001 << 3) ;
        if (pTxCtrl->Txq[2 ].Busy) {
            ClearQueuedPri(2 );
        }
        MessageDeleteTx(2 , 1 );
        break;
    default:
        *(vu16 *)((0x04808000) + 0x0B4) = (0x0001 << 0) ;
        break;
    }
    if (pTxCtrl->Txq[0 ].Busy) {
        ClearQueuedPri(0 );
    }
    MessageDeleteTx(0 , 1 );
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
void DeleteTxFrames(u32 camAdrs)
{
    WlMaDataReq *pReq, *pNextReq;
    LPTXFRM pFrm;
    u32 bTask = 0 ;
    u32 i;
    if (CAM_GetFrameCount(camAdrs) == 0) {
        return;
    }
    for (i = 0; i < 3; i++) {
        pReq = (WlMaDataReq *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[i]).Head) ;
        if ((u32)pReq == (u32)(-1) ) {
            continue;
        }
        do {
            pNextReq = (WlMaDataReq *)GetHeapBufNextAdrs(pReq);
            pFrm = (LPTXFRM)&pReq->frame;
            if (pFrm->FirmHeader.CamAdrs == camAdrs) {
                if ((i == 1) || (pFrm == ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[i].pFrm)) {
                    CAM_DecFrameCount(pFrm);
                    pFrm->FirmHeader.CamAdrs = 0;
                    CAM_IncFrameCount(pFrm);
                } else {
                    pFrm->MacHeader.Tx.Status = 2;
                    CAM_DecFrameCount(pFrm);
                    IssueMaDataConfirm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[i], pReq);
                    if (bTask == 0 ) {
                        bTask = 1 ;
                    }
                }
            }
            pReq = pNextReq;
        } while ((u32)pReq != (u32)(-1) );
    }
}
void DeleteTxFrameByAdrs(u16 *pMacAdrs)
{
    LPCAM_ELEMENT pCAM = (LPCAM_ELEMENT)((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM;
    u32 i;
    if (pMacAdrs[0] & 0x0001) {
        for (i = 1, pCAM++; i < ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum; i++, pCAM++) {
            DeleteTxFrames(i);
        }
    }
    else {
        i = CAM_Search(pMacAdrs);
        if (i != 255 ) {
            DeleteTxFrames(i);
        }
        if ((((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Mode == 1 ) && (CAM_GetStaState(i) == 0x40 )) {
