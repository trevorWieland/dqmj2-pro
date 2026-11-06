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
static void RxReAssResFrame(LPREASSRES_FRAME pFrm)
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
static void RxProbeReqFrame(LPPRBREQ_FRAME pFrm)
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
static void RxProbeResFrame(LPPRBRES_FRAME pFrm, LPELEMENT_CHECKER pChk)
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
        }
        pDesc->rateSet.basic = pChk->rateSet.Basic;
        pDesc->rateSet.support = pChk->rateSet.Support;
        pDesc->channel = pChk->channel;
        if (pChk->pCFP != 0 ) {
            pDesc->cfpPeriod = WL_ReadByte(&pChk->pCFP->CFPPeriod);
        }
        if (pChk->pTIM != 0 ) {
            pDesc->dtimPeriod = WL_ReadByte(&pChk->pTIM->DTIMPeriod);
        }
        pCfm->header.length += pDesc->length;
        pCfm->bssDescCount++;
        pMLME->Work.Scan.MaxConfirmLength -= pDesc->length;
        if (pMLME->Work.Scan.MaxConfirmLength < (sizeof(WlBssDesc) - 4) / 2) {
            ClearTimeOut();
            pMLME->State = (0x05 | 0x10) ;
            AddTask(2 , 0 );
        }
    } else {
        WSetMacAdrs1(pDesc->bssid, (u16 *)NULL_ADRS);
    }
}
static void RxAuthFrame(LPAUTH_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    LPAUTH_BODY pAuth;
    LPAUTH_FRAME pTxFrm;
    u32 bodyLen, cam_adrs;
    u32 bTxAuth;
    u16 seqNum, txtLen, stsCode;
    bodyLen = pFrm->FirmHeader.Length;
    pAuth = &pFrm->Body;
    ;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000008 ) {
        LPTXQ pTxq = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq;
        u16 map = *(vu16 *)((0x04808000) + 0x0B0) ;
        if ((((map & (0x0001 << 0) ) == 0) || (pTxq[0].Busy == 0)) && (((map & (0x0001 << 2) ) == 0) || (pTxq[1].Busy == 0)) && (((map & (0x0001 << 3) ) == 0) || (pTxq[2].Busy == 0)) && ((*(vu16 *)((0x04808000) + 0x19C) & (0x0001 << 0) ) == 0)) {
            *(vu16 *)((0x04808000) + 0x032) = 0x0000;
            *(vu16 *)((0x04808000) + 0x032) = 0x8000;
            ((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl.IcvOkCntFlag = 0;
        }
    }
    if (IsExistManFrame(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x0B * 0x0010)) )) {
        return;
    }
    bTxAuth = 0 ;
    txtLen = 0;
    seqNum = pAuth->SeqNum + 1;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    if (cam_adrs == 0) {
        stsCode = 19 ;
        bTxAuth = 1 ;
    } else {
        if (pWork->Mode == 1 ) {
            if (CAM_GetStaState(cam_adrs) > 0x20 ) {
                CAM_SetStaState(cam_adrs, 0x20 );
                MLME_IssueDeAuthIndication(pFrm->Dot11Header.SA, 1 );
            }
            if ((pFrm->MacHeader.Rx.Status & (0x0001 << 10) ) && (CAM_GetAuthSeed(cam_adrs) != 0)) {
                pAuth->AlgoType = 1 ;
                stsCode = 15 ;
                seqNum = 4;
                bTxAuth = 1 ;
                CAM_SetAuthSeed(cam_adrs, 0);
                goto tx_auth;
            }
        }
        switch (pAuth->AlgoType) {
        case 0 :
            if ((pWork->Mode == 1 ) && (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.AuthAlgo == 1 )) {
                stsCode = 13 ;
                bTxAuth = 1 ;
                break;
            }
            if (pWork->Mode == 1 ) {
                if (pAuth->SeqNum == 1) {
                    ;
                    stsCode = 0 ;
                    bTxAuth = 1 ;
                } else {
                    stsCode = 14 ;
                    seqNum = 2;
                    bTxAuth = 1 ;
                }
            }
            else if ((pWork->Mode != 1 ) && (pAuth->SeqNum == 2)) {
                ;
                if ((pMLME->pReq.Auth->algorithm == 0 ) && MatchMacAdrs(pMLME->pReq.Auth->peerMacAdrs, pFrm->Dot11Header.SA)) {
                    if (pMLME->State == (0x01 | 0x30) ) {
                        ClearTimeOut();
                        if (pAuth->StatusCode == 0x00 ) {
                            WSetStaState(0x30 );
                            pMLME->pCfm.Auth->resultCode = 0x00 ;
                            pMLME->pCfm.Auth->statusCode = 0x00 ;
                        } else {
                            pMLME->pCfm.Auth->resultCode = 0x0C ;
                            pMLME->pCfm.Auth->statusCode = pAuth->StatusCode;
                        }
                        pMLME->State = (0x05 | 0x30) ;
                        AddTask(2 , 2 );
                    }
                } else {
                }
            }
            break;
        case 1 :
            if (pWork->Mode == 1 ) {
                CAM_SetStaState(cam_adrs, 0x20 );
                if (pAuth->SeqNum == 1) {
                    ;
                    pTxFrm = MakeAuthFrame(pFrm->Dot11Header.SA, 128 , 1 );
                    if ((u32)pTxFrm != (0) ) {
                        pTxFrm->Body.AlgoType = pAuth->AlgoType;
                        pTxFrm->Body.SeqNum = seqNum;
                        pTxFrm->Body.StatusCode = 0;
                        SetChallengeText(cam_adrs, pTxFrm);
                        TxManCtrlFrame((LPTXFRM)pTxFrm);
                    }
                }
                else if (pAuth->SeqNum == 3) {
                    ;
                    if ((CAM_GetStaState(cam_adrs) != 0x20 ) || (CAM_GetAuthSeed(cam_adrs) == 0)) {
                        stsCode = 1 ;
                        bTxAuth = 1 ;
                        break;
                    }
                    if (CheckChallengeText(pFrm) == 0 ) {
                        stsCode = 15 ;
                        bTxAuth = 1 ;
                        CAM_SetAuthSeed(cam_adrs, 0);
                        break;
                    }
                    CAM_SetAuthSeed(cam_adrs, 0);
                    stsCode = 0 ;
                    bTxAuth = 1 ;
                }
                else {
                    CAM_SetAuthSeed(cam_adrs, 0);
                    stsCode = 14 ;
                    seqNum = 2;
                    bTxAuth = 1 ;
                }
                break;
            }
            else {
                if ((pMLME->pReq.Auth->algorithm != 1 ) || (MatchMacAdrs(pMLME->pReq.Auth->peerMacAdrs, pFrm->Dot11Header.SA) == 0)) {
                    break;
                }
                if (pAuth->SeqNum == 2) {
                    ;
                    if (pMLME->State == (0x01 | 0x30) ) {
                        if (pAuth->StatusCode != 0 ) {
                            ClearTimeOut();
                            pMLME->State = (0x05 | 0x30) ;
                            pMLME->pCfm.Auth->resultCode = 0x0C ;
                            pMLME->pCfm.Auth->statusCode = pAuth->StatusCode;
                            AddTask(2 , 2 );
                            WSetStaState(0x20 );
                        } else {
                            pMLME->State = (0x03 | 0x30) ;
                            pTxFrm = MakeAuthFrame(pFrm->Dot11Header.SA, WL_ReadByte(&pFrm->Body.ChallengeText.Length), 1 );
                            if ((u32)pTxFrm != (0) ) {
                                pTxFrm->Dot11Header.FrameCtrl.Bit.WEP = 1;
                                MI_CpuCopy16((void *)(u32)&pFrm->Body, (void *) (u32)&pTxFrm->Body, pFrm->FirmHeader.Length + 1) ;
                                pTxFrm->Body.AlgoType = pAuth->AlgoType;
                                pTxFrm->Body.SeqNum = 3;
                                pTxFrm->Body.StatusCode = 0;
                                TxManCtrlFrame((LPTXFRM)pTxFrm);
                            }
                        }
                    }
                }
                else if (pAuth->SeqNum == 4) {
                    ;
                    if (pMLME->State == (0x03 | 0x30) ) {
                        ClearTimeOut();
                        if (pAuth->StatusCode == 0x00 ) {
                            WSetStaState(0x30 );
                            pMLME->pCfm.Auth->resultCode = 0x00 ;
                            pMLME->pCfm.Auth->statusCode = 0x00 ;
                        } else {
                            pMLME->pCfm.Auth->resultCode = 0x0C ;
                            pMLME->pCfm.Auth->statusCode = pAuth->StatusCode;
                        }
                        pMLME->State = (0x05 | 0x30) ;
                        AddTask(2 , 2 );
                    }
                }
                else {
                }
            }
            break;
        default:
            ;
            if (pWork->Mode == 1 ) {
                stsCode = 13 ;
                bTxAuth = 1 ;
            }
            break;
        }
    }
tx_auth:
    if (bTxAuth) {
        pTxFrm = MakeAuthFrame(pFrm->Dot11Header.SA, txtLen, (stsCode != 0 ));
        if ((u32)pTxFrm != (0) ) {
            pTxFrm->Body.AlgoType = pAuth->AlgoType;
            pTxFrm->Body.SeqNum = seqNum;
            pTxFrm->Body.StatusCode = stsCode;
            TxManCtrlFrame((LPTXFRM)pTxFrm);
        }
    }
