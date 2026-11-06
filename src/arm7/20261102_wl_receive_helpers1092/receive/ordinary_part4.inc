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
            pCounterContext->Counter.rx.duplicateErr++;
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
                        pWork->DTIMCount = dtimCnt;
                    }
                    pWork->bExistTIM = 0x00 ;
                    if (dtimCnt == 0) {
                        if (WL_ReadByte(&elementCheck.pTIM->BitmapCtrl) & 0x01) {
                            pWork->bExistTIM |= 0x01 ;
                        }
                    }
                    n = WL_ReadByte(&elementCheck.pTIM->BitmapCtrl) & 0x00FEUL;
                    n1 = n * 8;
                    n2 = (n + WL_ReadByte(&elementCheck.pTIM->Length) - 3) * 8;
                    if ((n1 <= pWork->AID) && (pWork->AID <= n2)) {
                        ofst = pWork->AID - n1;
                        bit = ofst & 0x07;
                        ofst = ofst / 8;
                        if (WL_ReadByte(&elementCheck.pTIM->VitrualBitmap[ofst]) & (0x01 << bit)) {
                            pWork->bExistTIM |= 0x02 ;
                            TxPsPollFrame();
                        }
                    }
                    if ((pHeapMan->TxPri[0 ].Count == 0) && (pHeapMan->TxPri[1 ].Count == 0) && (pWork->bExistTIM == 0x00 )) {
                        {
                            WSetPowerState((0x0001 << 0) );
                        }
                    }
                }
            }
            if (pConfig->BcnTxRxIndMsg) {
                MLME_IssueBeaconRecvIndication(pFrm);
            }
            ;
        }
    }
    if (elementCheck.pSSID != 0 ) {
        UpdateApList(elementCheck.channel, pFrm, elementCheck.pSSID);
    }
}
void RxDisAssFrame(LPDISASS_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPDEAUTH_FRAME pDeAuth;
    u32 st, cam_adrs;
    ;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    switch (pWork->Mode) {
    case 1 :
        st = CAM_GetStaState(cam_adrs);
        if (st == 0x40 ) {
            CAM_SetStaState(cam_adrs, 0x30 );
            MLME_IssueDisAssIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
            DeleteTxFrames(cam_adrs);
        } else {
            if (st == 0x30 ) {
                pDeAuth = (LPDEAUTH_FRAME)MakeDisAssFrame(pFrm->Dot11Header.SA, 7 );
            } else {
                pDeAuth = MakeDeAuthFrame(pFrm->Dot11Header.SA, 7 , 1 );
            }
            if ((u32)pDeAuth != (0) ) {
                TxManCtrlFrame((LPTXFRM)pDeAuth);
            }
        }
        break;
    case 2 :
    case 3 :
        if ((pWork->STA == 0x40 ) && (MatchMacAdrs(pFrm->Dot11Header.SA, pWork->LinkAdrs))) {
            WSetStaState(0x30 );
            WClearAids();
            MLME_IssueDisAssIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
        }
        break;
    }
}
void RxAssReqFrame(LPASSREQ_FRAME pFrm)
{
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    LPASSREQ_BODY pAssReq;
    LPDEAUTH_FRAME pTxDeAuthFrm;
    LPASSRES_FRAME pTxFrm;
    u32 bodyLen;
    u16 stsCode, aid, cam_adrs;
    ELEMENT_CHECKER elementCheck;
    bodyLen = pFrm->FirmHeader.Length;
    pAssReq = &(pFrm->Body);
    aid = 0;
    if (bodyLen <= 2 + 2) {
        return;
    }
    ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode != 1 ) {
        ;
        return;
    }
    if (IsExistManFrame(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x01 * 0x0010)) )) {
        return;
    }
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    do {
        if ((cam_adrs == 0) || (CAM_GetStaState(cam_adrs) < 0x30 )) {
            if (IsExistManFrame(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x0C * 0x0010)) )) {
                return;
            }
            pTxDeAuthFrm = MakeDeAuthFrame(pFrm->Dot11Header.SA, 6 , 1 );
            if ((u32)pTxDeAuthFrm != (0) ) {
                TxManCtrlFrame((LPTXFRM)pTxDeAuthFrm);
            }
            return;
        }
        if (CAM_GetStaState(cam_adrs) == 0x40 ) {
            CAM_SetStaState(cam_adrs, 0x30 );
            MLME_IssueDisAssIndication(pFrm->Dot11Header.SA, 1 );
        } else if (CAM_GetAID(cam_adrs) != 0) {
            ;
            return;
        }
        MI_CpuClear32(&elementCheck, sizeof(elementCheck));
        elementCheck.pElement = pAssReq->Buf;
        elementCheck.bodyLength = bodyLen - (2 + 2);
        ElementChecker(&elementCheck);
        if ((pAssReq->CapaInfo.Data & 0xFFC2 ) || (pAssReq->CapaInfo.Bit.ESS == 0) || ((pConfig->WepMode == 0 ) && (pAssReq->CapaInfo.Bit.Privacy == 1)) || ((pConfig->WepMode != 0 ) && (pAssReq->CapaInfo.Bit.Privacy == 0)) || ((pConfig->PreambleType == 1 ) && (pAssReq->CapaInfo.Bit.ShortPreamble == 0))) {
            stsCode = 10 ;
            break;
        }
        CAM_SetCapaInfo(cam_adrs, pAssReq->CapaInfo.Data);
        if ((elementCheck.matchFlag & 0x0001 ) == 0) {
            stsCode = 1 ;
            break;
        }
        if ((elementCheck.matchFlag & 0x0004 ) == 0) {
            stsCode = 18 ;
            break;
        }
        CAM_SetSupRate(cam_adrs, elementCheck.rateSet.Support);
        stsCode = 0 ;
    } while (0 );
    pTxFrm = MakeAssResFrame(cam_adrs, stsCode, elementCheck.pSSID);
    if ((u32)pTxFrm != (0) ) {
        TxManCtrlFrame((LPTXFRM)pTxFrm);
    }
}
static void RxAssResFrame(LPASSRES_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    LPASSRES_BODY pAssRes;
    u32 bodyLen;
    bodyLen = pFrm->FirmHeader.Length;
    pAssRes = &pFrm->Body;
    ;
    if ((pWork->Mode != 2 ) && (pWork->Mode != 3 )) {
        ;
        return;
    }
    if (pMLME->State == (0x01 | 0x50) ) {
        if (MatchMacAdrs(pMLME->pReq.Ass->peerMacAdrs, pFrm->Dot11Header.SA)) {
            ClearTimeOut();
            if (pAssRes->StatusCode == 0 ) {
                WSetAids(pAssRes->AID & 0x0FFF);
                MakePsPollFrame(pWork->AID);
                WSetMacAdrs1(pWork->LinkAdrs, pFrm->Dot11Header.SA);
                pWork->APCamAdrs = CAM_Search(pFrm->Dot11Header.SA);
                CAM_SetStaState(pWork->APCamAdrs, 0x40 );
            }
            if (pAssRes->StatusCode == 0x00 ) {
                pMLME->pCfm.Ass->resultCode = 0x00 ;
                pMLME->pCfm.Ass->statusCode = 0x00 ;
                WSetStaState(0x40 );
            } else {
                pMLME->pCfm.Ass->resultCode = 0x0C ;
                pMLME->pCfm.Ass->statusCode = pAssRes->StatusCode;
            }
            pMLME->pCfm.Ass->aid = pWork->AID;
            pMLME->State = (0x03 | 0x50) ;
            AddTask(2 , 3 );
        }
    }
}
static void RxReAssReqFrame(LPREASSREQ_FRAME pFrm)
{
    LPWL_MAN pWlMan = (LPWL_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    LPREASSREQ_BODY pReAssReq;
    LPDEAUTH_FRAME pTxDeAuthFrm;
    LPREASSRES_FRAME pTxFrm;
    u32 bodyLen;
    u16 stsCode, aid, cam_adrs;
    ELEMENT_CHECKER elementCheck;
    bodyLen = pFrm->FirmHeader.Length;
    pReAssReq = &pFrm->Body;
    aid = 0;
    if (bodyLen <= 2 + 2 + 6) {
        return;
    }
    ;
    if (pWlMan->Work.Mode != 1 ) {
        ;
        return;
    }
    if (IsExistManFrame(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x03 * 0x0010)) )) {
        return;
    }
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    do {
        if (CAM_GetStaState(cam_adrs) < 0x30 ) {
            if (IsExistManFrame(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x0C * 0x0010)) )) {
                return;
            }
            pTxDeAuthFrm = MakeDeAuthFrame(pFrm->Dot11Header.SA, 6 , 1 );
            if ((u32)pTxDeAuthFrm != (0) ) {
                TxManCtrlFrame((LPTXFRM)pTxDeAuthFrm);
