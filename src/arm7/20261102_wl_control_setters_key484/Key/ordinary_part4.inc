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

void TxqEndData(LPTXFRM pFrm, u32 flag)
{
    LPHEAPBUF_MAN pBufMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[0 ];
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPWL_MAN pCounterContext = ((LPWL_MAN)native_host_arm7_data_0380fff4);
    void *pReq = (void *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    CAM_DecFrameCount(pFrm);
    if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
        pCounterContext->Counter.tx.success++;
        if (pFrm->Dot11Header.FrameCtrl.Bit.ToDS) {
            if (pFrm->Dot11Header.Adrs3[0] & 0x0001) {
                pCounterContext->Counter.tx.multicast++;
            } else {
                pCounterContext->Counter.tx.unicast++;
            }
        } else {
            if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                pCounterContext->Counter.tx.multicast++;
            } else {
                pCounterContext->Counter.tx.unicast++;
            }
        }
    } else {
        pCounterContext->Counter.tx.failed++;
    }
    if (pFrm->Dot11Header.FrameCtrl.Bit.WEP) {
        pCounterContext->Counter.tx.wep++;
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
    LPWL_MAN pCounterContext = ((LPWL_MAN)native_host_arm7_data_0380fff4);
    LPHEAPBUF_MAN pBufMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[1 ];
    LPAUTH_FRAME pAuth;
    LPASSRES_FRAME pAssRes;
    LPDISASS_FRAME pDisAss;
    LPDEAUTH_FRAME pDeAuth;
    u32 bRelease = 1 ;
    u32 i, type, cam_adrs;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    if ((pFrm->MacHeader.Tx.Status & (0x0001 << 1) ) == 0) {
        pCounterContext->Counter.tx.success++;
        if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
            pCounterContext->Counter.tx.multicast++;
        } else {
            pCounterContext->Counter.tx.unicast++;
        }
        if (CAM_GetPowerMgtMode(cam_adrs)) {
            if ((pFrm->Dot11Header.FrameCtrl.Data & 0x2000 ) == 0) {
                CAM_SetDoze(cam_adrs);
            }
        }
    } else {
        pCounterContext->Counter.tx.failed++;
    }
    if (pFrm->Dot11Header.FrameCtrl.Bit.WEP) {
        pCounterContext->Counter.tx.wep++;
    }
    pCounterContext->Counter.tx.retry += LoadLow(&pFrm->MacHeader.Tx.rsv_RetryCount);
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
                    SetManCtrlFrame((LPTXFRM)pDeAuth);
                    TxqPri(1);
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

void TxEndKeyData(LPTXQ pTxq)
{
    u32 retrycnt = LoadLow(&pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount);
    LPWL_MAN pCounterContext = ((LPWL_MAN)native_host_arm7_data_0380fff4);
    if (retrycnt == 0) {
        ;
        pCounterContext->Counter.multiPoll.txNull++;
    } else {
        ;
        pCounterContext->Counter.multiPoll.txKey += retrycnt;
    }
    pTxq->OutCount++;
    pTxq->Busy = 0 ;
}

void TxManCtrlFrame(LPTXFRM pFrm)
{
    SetManCtrlFrame(pFrm);
    TxqPri(1 );
}

void SetManCtrlFrame(LPTXFRM pFrm)
{
    pFrm->FirmHeader.CamAdrs = CAM_Search(pFrm->Dot11Header.Adrs1);
    if (pFrm->FirmHeader.CamAdrs == 255 ) {
        pFrm->FirmHeader.CamAdrs = 0;
    }
    pFrm->FirmHeader.FrameTime = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.IntervalCount;
    if (pFrm->Dot11Header.FrameCtrl.Data & 0x4000 ) {
        pFrm->MacHeader.Tx.MPDU += 8;
    }
    CAM_IncFrameCount(pFrm);
    MoveHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[1 ], (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
}

static u32 IsEnableManagement(void)
{
    if (((*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[1]).Count) < (24 - ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.ConnectSta)) {
        return 1 ;
    }
    ;
    return 0 ;
}

LPDEAUTH_FRAME MakeDeAuthFrame(u16 *pDA, u16 reasonCode, u32 bCheck)
{
    WlMaDataReq *pReq;
    LPDEAUTH_FRAME pFrm;
    ;
    if (bCheck && !IsEnableManagement()) {
        ;
        return (0) ;
    }
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(DEAUTH_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPDEAUTH_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPDEAUTH_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.ReasonCode = reasonCode;
    pFrm->FirmHeader.Length = 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x0C * 0x0010)) ;
    return pFrm;
}

void InitManHeader(LPTXFRM pFrm, u16 *pDA)
{
    MI_CpuClear16(pFrm, (sizeof(FIRM_HEADER) + sizeof(MAC_HEADER) + sizeof(MAN_HEADER)) );
    pFrm->MacHeader.Tx.Service_Rate = WCalcManRate();
    WSetMacAdrs3(pFrm->Dot11Header.Adrs1, pDA, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MacAdrs, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID);
}
