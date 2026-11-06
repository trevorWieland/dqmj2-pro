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
    pCounter += LoadHigh(&pFrm->MacHeader.Tx.rsv_RetryCount);
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

void MakeBeaconFrame(void)
{
    LPTXFRM_MAC pFrm = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.pMacFrm;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPBEACON_BODY pBody;
    u8 *pBuf;
    u8 *p;
    u32 i, vtsf;
    u16 *p16;
    p16 = (u16 *)&pFrm->MacHeader.Tx;
    *p16++ = 0;
    *p16++ = 0;
    *p16++ = 0;
    *p16++ = 0;
    *p16++ = WCalcManRate();
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x08 * 0x0010)) ;
    pFrm->Dot11Header.DurationID = 0;
    WSetMacAdrs3(pFrm->Dot11Header.Adrs1, (u16 *)BC_ADRS, pConfig->MacAdrs, pConfig->MacAdrs);
    pFrm->Dot11Header.SeqCtrl.Data = 0;
    pBody = (LPBEACON_BODY)pFrm->Body;
    pBody->TimeStamp[0] = 0;
    pBody->TimeStamp[1] = 0;
    pBody->BeaconInterval = pWork->BeaconPeriod;
    pBody->CapaInfo.Data = pWork->CapaInfo;
    pBuf = pBody->Buf;
    if (pConfig->BeaconType == 0 ) {
        pWork->Ofst.Beacon.SSID = (u16)((u32)pBuf - (u32)pFrm->Body);
        WL_WriteByte(pBuf++, 0 );
        WL_WriteByte(pBuf++, pWork->SSIDLength);
        for (i = 0; i < pWork->SSIDLength; i++) {
            WL_WriteByte(pBuf++, WL_ReadByte(&pWork->SSID[i]));
        }
        WL_WriteByte(&pBuf[-i - 1], i);
    } else {
