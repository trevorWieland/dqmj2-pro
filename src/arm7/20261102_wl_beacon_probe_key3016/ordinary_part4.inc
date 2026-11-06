    OSAlarm Alarm;
    OSAlarm KeyAlarm;
    u32 WlDbgLevel;
    u16 WlOperation;
    u16 EnableChannel;
} WL_MAN, *LPWL_MAN;
void RxDataFrameTask(void)
{
    LPDEAUTH_FRAME pDeAuth;
    WlMaDataInd *pInd;
    LPRXFRM pFrm;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    u32 camAdrs, err;
    pInd = (WlMaDataInd *)((u32)(*(LPHEAPBUF_MAN)&pHeapMan->RxData).Head) ;
    if ((u32)pInd == (u32)(-1) ) {
        return;
    }
    if (pWork->STA != 0x40 ) {
        ReleaseHeapBuf(&pHeapMan->RxData, pInd);
        return;
    }
    pFrm = (LPRXFRM)&pInd->frame;
    if (pFrm->Dot11Header.FrameCtrl.Bit.ToDS) {
        if (pFrm->Dot11Header.Adrs3[0] & 0x0001) {
            pCounter->rx.multicast++;
        } else {
            pCounter->rx.unicast++;
        }
    } else {
        if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
            pCounter->rx.multicast++;
        } else {
            pCounter->rx.unicast++;
        }
    }
    pCounter->rx.fragment += (((pFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) - 1);
    err = 1;
    switch (pWork->Mode) {
    case 1 :
        if (pFrm->Dot11Header.FrameCtrl.Data & (0x0100 | 0x0200 ) != 0x0100 ) {
            ;
            break;
        }
        camAdrs = CAM_Search(pFrm->Dot11Header.Adrs2);
        if ((camAdrs == 255 ) || (CAM_GetStaState(camAdrs) != 0x40 )) {
            if (CAM_GetStaState(camAdrs) == 0x30 ) {
                if (IsExistManFrame(pFrm->Dot11Header.Adrs2, ((0x00 * 0x0004) | (0x0A * 0x0010)) )) {
                    break;
                }
                pDeAuth = (LPDEAUTH_FRAME)MakeDisAssFrame(pFrm->Dot11Header.Adrs2, 7 );
            } else {
                if (IsExistManFrame(pFrm->Dot11Header.Adrs2, ((0x00 * 0x0004) | (0x0C * 0x0010)) )) {
                    break;
                }
                pDeAuth = MakeDeAuthFrame(pFrm->Dot11Header.Adrs2, 7 , 1 );
            }
            if ((u32)pDeAuth != (0) ) {
                TxManCtrlFrame((LPTXFRM)pDeAuth);
            }
            break;
        }
        CAM_SetPowerMgtMode(camAdrs, pFrm->Dot11Header.FrameCtrl.Bit.PowerMan);
        if (pFrm->Dot11Header.SeqCtrl.Data == CAM_GetLastSeqCtrl(camAdrs)) {
            pCounter->rx.duplicateErr++;
            break;
        }
        WSetMacAdrs1(pFrm->Dot11Header.Adrs1, pFrm->Dot11Header.Adrs3);
        err = 0;
        break;
    case 2 :
    case 3 :
        if (pFrm->Dot11Header.FrameCtrl.Data & (0x0100 | 0x0200 ) != 0x0100 ) {
            ;
            break;
        }
        if (pWork->PowerMgtMode != 0x00 ) {
            if ((pFrm->Dot11Header.FrameCtrl.Data & 0x2000 ) == 0) {
                if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                    pWork->bExistTIM &= ~0x01 ;
                } else {
                    if (pWork->Mode != 3 ) {
                        pWork->bExistTIM &= ~0x02 ;
                    }
                }
                if ((pWork->bExistTIM == 0x00 ) && (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[0]).Count) == 0) && (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[1]).Count) == 0)) {
                    {
                        WSetPowerState((0x0001 << 0) );
                    }
                }
            }
        }
        camAdrs = pWork->APCamAdrs;
        if (pFrm->Dot11Header.SeqCtrl.Data == CAM_GetLastSeqCtrl(camAdrs)) {
            pCounter->rx.duplicateErr++;
            break;
        }
        WSetMacAdrs1(pFrm->Dot11Header.Adrs2, pFrm->Dot11Header.Adrs3);
        err = 0;
        break;
    }
    if (err == 0) {
        ;
        pFrm->FirmHeader.CamAdrs = camAdrs;
        CAM_SetRSSI(camAdrs, LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI));
        CAM_SetLastSeqCtrl(camAdrs, pFrm->Dot11Header.SeqCtrl.Data);
        CAM_UpdateLifeTime(camAdrs);
        pFrm->FirmHeader.Length = pFrm->MacHeader.Rx.MPDU - 24;
        pInd->header.code = (0x0100 | 0x80) ;
        pInd->header.length = ((pFrm->FirmHeader.Length + sizeof(WlRxFrame) - 4+1)/2) ;
        ;
        SendMessageToWmDirect(&pHeapMan->RxData, pInd);
        ;
    } else {
        ReleaseHeapBuf(&pHeapMan->RxData, pInd);
    }
    if (((*(LPHEAPBUF_MAN)&pHeapMan->RxData).Count) != 0) {
        AddTask(2 , 6 );
    }
}
u32 RxMpFrame(LPRXFRM pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl;
    WlMaMpInd *pInd;
    u32 cnt;
    u16 bitmap, out;
    if (pWork->STA != 0x40 ) {
        return 1;
    }
    if ((MatchMacAdrs(pFrm->Dot11Header.Adrs2, pWork->BSSID) == 0) || (MatchMacAdrs(pFrm->Dot11Header.Adrs3, pWork->LinkAdrs) == 0)) {
        return 1;
    }
    ;
    ;
    bitmap = 0x0001 << pWork->AID;
    if ((bitmap & ((WlRxMpFrame *)pFrm)->bitmap) == 0) {
        ;
        pRxCtrl->TxKeyReg = 0;
        ;
    } else {
        pRxCtrl->TxKeyReg = (0x0001 << 13) ;
    }
    out = *(vu16 *)((0x04808000) + 0x098) ;
    if ((out & 0x8000) && (((LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(out & 0x7FFF) * 2)) )->MacHeader.Tx.rsv_RetryCount != 0)) {
        pRxCtrl->TxKeyReg |= (0x0001 << 14) ;
    }
    CAM_UpdateLifeTime(pWork->APCamAdrs);
    pFrm->FirmHeader.Length = pFrm->MacHeader.Rx.MPDU - 24 - 2 - 2;
    pInd = (WlMaMpInd *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    pInd->header.code = (0x0100 | 0x82) ;
    pInd->header.length = ((pFrm->FirmHeader.Length + sizeof(WlRxMpFrame) - 2+1)/2) ;
    bitmap = pInd->frame.bitmap;
    for (cnt = 0; bitmap != 0; bitmap >>= 1) {
        if (bitmap & 1) {
            cnt++;
        }
    }
    pInd->frame.txKeySts |= (pRxCtrl->TxKeyReg | ((*(vu16 *)((0x04808000) + 0x098) & 0x8000) >> 4) | ((*(vu16 *)((0x04808000) + 0x094) & 0x8000) >> 3));
    pInd->frame.ackTimeStamp = pInd->frame.timeStamp + ((cnt * (pInd->frame.txop + 10) + (10 + 96 + 32 * 4 + 3 + 15)) >> 4);
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pInd);
    ;
    return 0;
}
void RxKeyDataFrame(LPRXFRM pFrm)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    WlMpKey *pMpKey = &pTxCtrl->pMpEndInd->mpKey;
    WlMpKeyData *pKeyData;
    u32 camAdrs, aid;
    u16 bitmap;
    if (pTxCtrl->Mp.Busy == 0 ) {
        return;
    }
    if (!MatchMacAdrs(pFrm->Dot11Header.Adrs1, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID)) {
        ;
        return;
    }
    if (pFrm->MacHeader.Rx.MPDU - 24 > pMpKey->length - 8) {
        ;
        return;
    }
    camAdrs = CAM_Search(pFrm->Dot11Header.Adrs2);
    if ((camAdrs == 255 ) || ((camAdrs != 0) && (CAM_GetStaState(camAdrs) != 0x40 ))) {
        LPDEAUTH_FRAME pTxDeAuthFrm;
        ;
            ;
        if (IsExistManFrame(pFrm->Dot11Header.Adrs2, ((0x00 * 0x0004) | (0x0C * 0x0010)) )) {
            return;
        }
        pTxDeAuthFrm = MakeDeAuthFrame(pFrm->Dot11Header.Adrs2, 7 , 0 );
        if ((u32)pTxDeAuthFrm != (0) ) {
            pTxDeAuthFrm->FirmHeader.FrameId = 0x0002 ;
            TxManCtrlFrame((LPTXFRM)pTxDeAuthFrm);
        }
        ;
        return;
    }
    if (camAdrs == 0) {
        return;
    }
    CAM_SetPowerMgtMode(camAdrs, pFrm->Dot11Header.FrameCtrl.Bit.PowerMan);
    CAM_UpdateLifeTime(camAdrs);
    aid = CAM_GetAID(camAdrs);
    bitmap = 0x0001 << aid;
    if (bitmap & pTxCtrl->GetKeyMap) {
        ;
        return;
    }
    if ((bitmap & pTxCtrl->SetKeyMap) == 0) {
        ;
        return;
    }
    pTxCtrl->GetKeyMap |= bitmap;
    pMpKey->bitmap &= ~bitmap;
    pKeyData = (WlMpKeyData *)pMpKey->data;
    for (bitmap >>= 1; bitmap != 0x0001; bitmap >>= 1) {
        if (bitmap & pTxCtrl->SetKeyMap) {
            pKeyData = (WlMpKeyData *)((u32)pKeyData + (u32)pMpKey->length);
        }
    }
    pKeyData->length = pFrm->MacHeader.Rx.MPDU - 24;
    WL_WriteByte(&pKeyData->rssi, LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI));
    WL_WriteByte(&pKeyData->rate, LoadLow(&pFrm->MacHeader.Rx.Service_Rate));
    if (pKeyData->length != 0) {
        MI_CpuCopy16((void *)(u32)pFrm->Body, (void *) (u32)pKeyData->cdata, pKeyData->length + 1) ;
    }
}
u32 RxMpAckFrame(LPRXFRM pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaMpAckInd *pInd;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x40 ) {
        return 1;
    }
    if ((MatchMacAdrs(pFrm->Dot11Header.Adrs2, pWork->BSSID) == 0) || (MatchMacAdrs(pFrm->Dot11Header.Adrs3, pWork->LinkAdrs) == 0)) {
        ;
        return 1;
    }
    ;
    pFrm->FirmHeader.Length = pFrm->MacHeader.Rx.MPDU - 24 - 2 - 2;
    pInd = (WlMaMpAckInd *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    pInd->header.code = (0x0100 | 0x85) ;
    pInd->header.length = ((sizeof(WlRxMpAckFrame)+1)/2) ;
    pInd->ack.txKeySts |= (((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl.TxKeyReg | ((*(vu16 *)((0x04808000) + 0x098) & 0x8000) >> 4) | ((*(vu16 *)((0x04808000) + 0x094) & 0x8000) >> 3));
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pInd);
    ;
    return 0;
}
void RxBeaconFrame(LPBEACON_FRAME pFrm)
{
    LPBEACON_BODY pBeacon;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    ELEMENT_CHECKER elementCheck;
    u32 n, n1, n2, ofst, bit, bp;
    u32 BodyLen, cam_adrs;
    u64 lltsf;
    u16 t1[4], t2[4];
    u16 *ptsf;
    ;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.rx.beacon++;
    cam_adrs = CAM_SearchAdd(pFrm->Dot11Header.SA);
    pFrm->FirmHeader.CamAdrs = cam_adrs;
    if (cam_adrs == 255 ) {
        return;
    }
    CAM_SetRSSI(cam_adrs, pFrm->MacHeader.Rx.rsv_RSSI);
    pBeacon = &pFrm->Body;
    BodyLen = pFrm->FirmHeader.Length;
    if (BodyLen <= 8 + 2 + 2) {
        return;
    }
    MI_CpuClear32(&elementCheck, sizeof(elementCheck));
    elementCheck.pElement = pBeacon->Buf;
    elementCheck.bodyLength = BodyLen - (8 + 2 + 2);
    elementCheck.matchFlag = 0x0002 ;
    if (pWork->SSIDLength == 0) {
        elementCheck.matchFlag |= 0x0001 ;
    }
    elementCheck.foundFlag = 0x0008 | 0x0030 ;
    elementCheck.rxStatus = pFrm->MacHeader.Rx.Status;
    elementCheck.capability = pBeacon->CapaInfo.Data;
    ElementChecker(&elementCheck);
    ;
    if ((elementCheck.pCFP != 0 ) && (pFrm->Dot11Header.Duration & 0x8000)) {
        *(vu16 *)((0x04808000) + 0x10C) = (u16)WL_ReadByte(&elementCheck.pCFP->CFPDurRemain.u8[0]) + ((u16)WL_ReadByte(&elementCheck.pCFP->CFPDurRemain.u8[1]) << 8);
    }
    if ((pMLME->State == (0x03 | 0x10) ) && (pMLME->pReq.Scan->scanType == 1 )) {
        ;
        if ((elementCheck.matchFlag & (0x0001 | 0x0008 )) == (0x0001 | 0x0008 )) {
            RxProbeResFrame((LPPRBRES_FRAME)pFrm, &elementCheck);
        }
    }
    else if (elementCheck.matchFlag & 0x0008 ) {
        {
            ;
            if (pMLME->State == (0x01 | 0x20) ) {
                ClearTimeOut();
                ;
                if ((elementCheck.matchFlag & (0x0010 | 0x0020 )) != (0x0010 | 0x0020 )) {
                    pMLME->Work.Join.Result = 0x0C ;
                    pMLME->Work.Join.Status = 10 ;
                    ;
                }
                else if (pFrm->Body.BeaconInterval > 1000 ) {
                    pMLME->Work.Join.Result = 0x0C ;
                    pMLME->Work.Join.Status = 1 ;
                    ;
                }
                else {
                    pMLME->Work.Join.Result = 0x00 ;
                    if ((elementCheck.foundFlag & 0x0002 ) && !(elementCheck.matchFlag & 0x0002 )) {
                        ;
                        WSetChannel(elementCheck.channel, 0 );
                    }
                    CAM_SetSupRate(cam_adrs, elementCheck.rateSet.Support);
                    if (pWork->Mode == 2 ) {
                        if (elementCheck.pGMIF != 0 ) {
                            u32 actZone = (u32)WL_ReadByte(&elementCheck.pGMIF->ActZone[0]) + ((u32)WL_ReadByte(&elementCheck.pGMIF->ActZone[1]) << 8);
                            WSetActiveZoneTime(actZone, 1 );
                            *(u16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) = (u16)WL_ReadByte(&elementCheck.pGMIF->VTSF[0]) + ((u16)WL_ReadByte(&elementCheck.pGMIF->VTSF[1]) << 8);
                        } else {
                            WSetActiveZoneTime(0xFFFF, 1 );
                            *(u16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) = 0;
                        }
                    }
                    WSetDTIMPeriod(WL_ReadByte(&elementCheck.pTIM->DTIMPeriod));
                    pWork->DTIMCount = WL_ReadByte(&elementCheck.pTIM->DTIMCount);
                    WSetBeaconPeriod(pFrm->Body.BeaconInterval);
                    pWork->bSynchro = 1;
                    pWork->bFirstTbtt = 1;
                    if (pWork->Mode == 2 ) {
                        *(vu16 *)((0x04808000) + 0x048) = 3;
                    }
                    *(vu16 *)((0x04808000) + 0x038) |= (0x0001 << 0) ;
                }
                WSetMacAdrs1(pMLME->pCfm.Join->peerMacAdrs, pFrm->Dot11Header.SA);
                pMLME->State = (0x05 | 0x20) ;
                AddTask(2 , 1 );
            }
            switch (pWork->Mode) {
            case 2 :
                if (elementCheck.pGMIF != 0 ) {
                    WSetActiveZoneTime((u16)WL_ReadByte(&elementCheck.pGMIF->ActZone[0]) + ((u16)WL_ReadByte(&elementCheck.pGMIF->ActZone[1]) << 8), 0 );
                    *(u16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) = (u16)WL_ReadByte(&elementCheck.pGMIF->VTSF[0]) + ((u16)WL_ReadByte(&elementCheck.pGMIF->VTSF[1]) << 8);
                    pWork->GameInfoLength = WL_ReadByte(&elementCheck.pGMIF->Length) - 3 - 1 - 4;
                    if (pWork->GameInfoLength != 0) {
                        if ((u32)elementCheck.pGMIF & 1) {
                            MI_CpuCopy16((void *)(u32)&elementCheck.pGMIF->VTSF[1], (void *) (u32)pWork->GameInfoAdrs, pWork->GameInfoLength + 2) ;
                            pWork->GameInfoAlign = 1;
                        } else {
                            MI_CpuCopy16((void *)(u32)elementCheck.pGMIF->GameInfo, (void *) (u32)pWork->GameInfoAdrs, pWork->GameInfoLength + 1) ;
                            pWork->GameInfoAlign = 0;
                        }
                    }
                }
            case 3 :
                pWork->BeaconLostCnt = 0;
                CAM_UpdateLifeTime(cam_adrs);
                lltsf = *(u64 *)pFrm->Body.TimeStamp;
                bp = (u32)pWork->BeaconPeriod * 1024;
                lltsf /= bp;
                lltsf++;
                lltsf *= bp;
                ptsf = (u16 *)&lltsf;
                *(vu16 *)((0x04808000) + 0x0F6) = ptsf[3];
                *(vu16 *)((0x04808000) + 0x0F4) = ptsf[2];
                *(vu16 *)((0x04808000) + 0x0F2) = ptsf[1];
                *(vu16 *)((0x04808000) + 0x0F0) = ptsf[0] | 0x0001;
                if ((pWork->Mode == 2 ) && (pWork->bFirstTbtt)) {
                    lltsf -= (u64)bp;
                    n = OS_DisableInterrupts();
                    t1[0] = *(vu16 *)((0x04808000) + 0x0F8) ;
                    t1[1] = *(vu16 *)((0x04808000) + 0x0FA) ;
                    t1[2] = *(vu16 *)((0x04808000) + 0x0FC) ;
                    t1[3] = *(vu16 *)((0x04808000) + 0x0FE) ;
                    t2[0] = *(vu16 *)((0x04808000) + 0x0F8) ;
                    t2[1] = *(vu16 *)((0x04808000) + 0x0FA) ;
                    t2[2] = *(vu16 *)((0x04808000) + 0x0FC) ;
                    t2[3] = *(vu16 *)((0x04808000) + 0x0FE) ;
                    OS_RestoreInterrupts(n);
                    if (t1[0] < t2[0]) {
                        n = (u32)((*(u64 *)t1 - lltsf) / 1024);
                    } else {
                        n = (u32)((*(u64 *)t2 - lltsf) / 1024);
                    }
                    if (n < pConfig->ActiveZone) {
                        *(vu16 *)((0x04808000) + 0x134) = pConfig->ActiveZone - n;
                    } else {
                        *(vu16 *)((0x04808000) + 0x134) = 0;
                    }
                }
                if ((pWork->STA == 0x40 ) && (elementCheck.pTIM != 0 ) && (pWork->PowerMgtMode == 1 )) {
                    u16 dtimCnt = WL_ReadByte(&elementCheck.pTIM->DTIMCount);
                    if (pWork->DTIMCount != dtimCnt) {
                        ;
