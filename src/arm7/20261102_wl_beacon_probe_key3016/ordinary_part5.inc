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
void RxAssResFrame(LPASSRES_FRAME pFrm)
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
void RxReAssReqFrame(LPREASSREQ_FRAME pFrm)
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
        elementCheck.pElement = pReAssReq->Buf;
        elementCheck.bodyLength = bodyLen - (2 + 2 + 6);
        elementCheck.foundFlag = 0x0800 ;
        ElementChecker(&elementCheck);
        if ((pReAssReq->CapaInfo.Data & 0xFFC2 ) || ((pWlMan->Config.WepMode == 0 ) && (pReAssReq->CapaInfo.Bit.Privacy == 1)) || ((pWlMan->Config.WepMode != 0 ) && (pReAssReq->CapaInfo.Bit.Privacy == 0))) {
            stsCode = 10 ;
            break;
        }
        CAM_SetCapaInfo(cam_adrs, pReAssReq->CapaInfo.Data);
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
    pTxFrm = MakeReAssResFrame(cam_adrs, stsCode, elementCheck.pSSID);
    if ((u32)pTxFrm != (0) ) {
        TxManCtrlFrame((LPTXFRM)pTxFrm);
    }
}
void RxReAssResFrame(LPREASSRES_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    LPREASSRES_BODY pReAssRes;
    u32 bodyLen;
    bodyLen = pFrm->FirmHeader.Length;
    pReAssRes = &pFrm->Body;
    ;
    if ((pWork->Mode != 2 ) && (pWork->Mode != 3 )) {
        ;
        return;
    }
    if (pMLME->State == (0x01 | 0x60) ) {
        if (MatchMacAdrs(pMLME->pReq.ReAss->newApMacAdrs, pFrm->Dot11Header.SA)) {
            ClearTimeOut();
            if (pReAssRes->StatusCode == 0 ) {
                WSetAids(pReAssRes->AID & 0x0FFF);
                MakePsPollFrame(pWork->AID);
                WSetMacAdrs1(pWork->LinkAdrs, pFrm->Dot11Header.SA);
                pWork->APCamAdrs = CAM_Search(pFrm->Dot11Header.SA);
                CAM_SetStaState(pWork->APCamAdrs, 0x40 );
                WSetStaState(0x40 );
            }
            if (pReAssRes->StatusCode == 0x00 ) {
                pMLME->pCfm.ReAss->resultCode = 0x00 ;
                pMLME->pCfm.ReAss->statusCode = 0x00 ;
                WSetStaState(0x40 );
            } else {
                pMLME->pCfm.ReAss->resultCode = 0x0C ;
                pMLME->pCfm.ReAss->statusCode = pReAssRes->StatusCode;
            }
            pMLME->pCfm.ReAss->aid = pWork->AID;
            pMLME->State = (0x03 | 0x60) ;
            AddTask(2 , 4 );
        }
    }
}
void RxProbeReqFrame(LPPRBREQ_FRAME pFrm)
{
    LPPRBRES_FRAME pTxFrm;
    ELEMENT_CHECKER elementCheck;
    ;
    if (IsExistManFrame(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x05 * 0x0010)) )) {
        return;
    }
    if ((pFrm->Dot11Header.BSSID[0] & 0x0001) || (pFrm->MacHeader.Rx.Status & (0x0001 << 15) )) {
        MI_CpuClear32(&elementCheck, sizeof(elementCheck));
        elementCheck.pElement = pFrm->Body.Buf;
        elementCheck.bodyLength = pFrm->FirmHeader.Length;
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.BcSsidResponse == 0 ) {
            elementCheck.foundFlag = 0x0800 ;
        }
        ElementChecker(&elementCheck);
        if ((elementCheck.matchFlag & 0x0001 ) == 0x0001 ) {
            pTxFrm = MakeProbeResFrame(pFrm->Dot11Header.SA);
            if ((u32)pTxFrm != (0) ) {
                TxManCtrlFrame((LPTXFRM)pTxFrm);
            }
        }
    }
}
void RxProbeResFrame(LPPRBRES_FRAME pFrm, LPELEMENT_CHECKER pChk)
{
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    WlMlmeScanCfm *pCfm;
    LPPRBRES_BODY pPrbRes;
    WlBssDesc *pDesc;
    u32 bodyLen, i, j, id, len;
    ELEMENT_CHECKER elementCheck;
    u16 *pBssidMask;
    u8 *pSrc, *pDst;
    if (pMLME->State != (0x03 | 0x10) ) {
        return;
    }
    ;
    pCfm = pMLME->pCfm.Scan;
    pPrbRes = &pFrm->Body;
    pBssidMask = pMLME->pReq.Scan->bssidMask;
    for (i = 0; i < pMLME->pReq.Scan->bssidMaskCount; i++) {
        if (MatchMacAdrs(pBssidMask, pFrm->Dot11Header.BSSID)) {
            pCfm->foundMap |= (1L << i);
            return;
        }
        pBssidMask += 3;
    }
    pDesc = &pCfm->bssDescList[0];
    for (i = 0; i < pCfm->bssDescCount; i++) {
        if (MatchMacAdrs(pFrm->Dot11Header.BSSID, pDesc->bssid)) {
            return;
        }
        pDesc = (WlBssDesc *)((u32)pDesc + pDesc->length * 2);
    }
    MI_CpuClear16((void *)(u32)pDesc, (sizeof(WlBssDesc) - 4)) ;
    bodyLen = pFrm->FirmHeader.Length;
    if (bodyLen <= 8 + 2 + 2) {
        return;
    }
    if (pChk == 0 ) {
        MI_CpuClear32(&elementCheck, sizeof(elementCheck));
        elementCheck.pElement = pPrbRes->Buf;
        elementCheck.bodyLength = bodyLen - (8 + 2 + 2);
        elementCheck.matchFlag = 0x0001 | 0x0002 ;
        elementCheck.foundFlag = 0x0008 | 0x0030 ;
        elementCheck.rxStatus = pFrm->MacHeader.Rx.Status;
        elementCheck.capability = pPrbRes->CapaInfo.Data;
        ElementChecker(&elementCheck);
        pChk = &elementCheck;
    }
    ;
    if (pChk->pGMIF != 0 ) {
        pDesc->gameInfoLength = WL_ReadByte(&pChk->pGMIF->Length) - 3 - 1 - 4;
        pDesc->length = ((sizeof(WlBssDesc) - 4) + pDesc->gameInfoLength + 1) / 2;
    } else {
        pDesc->length = ((sizeof(WlBssDesc) - 4) + pChk->otherElementLength + 1) / 2;
    }
    if (((pChk->matchFlag & 0x0001 ) == 0x0001 ) && (((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.Work.Scan.MaxConfirmLength >= pDesc->length)) {
        pDesc->capaInfo = pPrbRes->CapaInfo.Data;
        WSetMacAdrs1(pDesc->bssid, pFrm->Dot11Header.BSSID);
        pDesc->beaconPeriod = pPrbRes->BeaconInterval;
        pDesc->rssi = LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI);
        if (pChk->pGMIF != 0 ) {
            for (j = 0; j < pDesc->gameInfoLength; j++) {
                WL_WriteByte(&pDesc->gameInfo[j], WL_ReadByte(&pChk->pGMIF->GameInfo[j]));
            }
        } else {
            pDesc->otherElementCount = pChk->otherElementCount;
            if (pChk->otherElementCount != 0) {
                pSrc = (u8 *)pPrbRes->Buf;
                pDst = (u8 *)pDesc->otherElement;
                for (i = 0; i < pChk->otherElementCount;) {
                    id = WL_ReadByte(&pSrc[0]);
                    len = WL_ReadByte(&pSrc[1]);
                    if ((id > 6 ) && ((u32)pSrc != (u32)pChk->pGMIF)) {
                        for (j = 0; j < len + 2; j++) {
                            WL_WriteByte(pDst, WL_ReadByte(pSrc));
                            pDst++;
                            pSrc++;
                        }
                        i++;
                    } else {
                        pSrc += (len + 2);
                    }
                }
            }
        }
        if (pChk->pSSID != 0 ) {
            pDesc->ssidLength = WL_ReadByte(&pChk->pSSID->Length);
            for (j = 0; j < pDesc->ssidLength; j++) {
                WL_WriteByte(&pDesc->ssid[j], WL_ReadByte(&pChk->pSSID->SSID[j]));
            }
        } else {
            pDesc->ssidLength = 0;
            for (j = 0; j < 32 ; j++) {
                WL_WriteByte(&pDesc->ssid[j], 0);
            }
