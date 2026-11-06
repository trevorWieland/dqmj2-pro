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
        WSetMacAdrs1(pDesc->bssid, (u16 *)native_host_arm7_table_null_adrs_027f74c0);
    }
}
void RxAuthFrame(LPAUTH_FRAME pFrm)
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
}
void RxDeAuthFrame(LPDEAUTH_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPDEAUTH_BODY pDeAuth;
    u32 bodyLen, cam_adrs;
    bodyLen = pFrm->FirmHeader.Length;
    pDeAuth = &pFrm->Body;
    ;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    switch (pWork->Mode) {
    case 1 :
        if (CAM_GetStaState(cam_adrs) > 0x20 ) {
            CAM_SetStaState(cam_adrs, 0x20 );
            MLME_IssueDeAuthIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
            DeleteTxFrames(cam_adrs);
        }
        break;
    case 2 :
    case 3 :
        if ((pWork->STA > 0x20 ) && (MatchMacAdrs(pFrm->Dot11Header.SA, pWork->LinkAdrs))) {
            WSetStaState(0x20 );
            WClearAids();
            MLME_IssueDeAuthIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
            break;
        }
    }
}
void RxPsPollFrame(LPPSPOLL_FRAME pFrm)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    u32 cam_adrs;
    ;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    if (CAM_GetStaState(cam_adrs) == 0x40 ) {
        CAM_SetAwake(cam_adrs);
        if (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[1]).Count) != 0) {
            TxqPri(1 );
        }
        if (((*(LPHEAPBUF_MAN)&pHeapMan->TxPri[0]).Count) != 0) {
            TxqPri(0 );
        }
    }
}
void RxCfEndFrame(LPCFEND_FRAME pFrm)
{
    ;
}
void ElementChecker(LPELEMENT_CHECKER p)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    u8 *pBuf;
    s32 i;
    u32 id, len;
    pBuf = p->pElement;
    p->channel = pWork->CurrChannel;
    if (p->foundFlag & 0x0800 ) {
        p->matchFlag |= 0x0001 ;
    }
    for (i = p->bodyLength; i > 0;) {
        id = WL_ReadByte(pBuf++);
        len = WL_ReadByte(pBuf++);
        switch (id) {
        case 0 :
            if (len <= 32 ) {
                p->foundFlag |= 0x0001 ;
                p->pSSID = (LPSSID_ELEMENT)&pBuf[-2];
                if ((len == 0) && (p->foundFlag & 0x0800 )) {
                    p->matchFlag |= 0x0001 ;
                } else {
                    p->matchFlag &= ~0x0001 ;
                    if (WCheckSSID(len, pBuf)) {
                        p->matchFlag |= 0x0001 ;
                    }
                }
            }
            break;
        case 1 :
            if (len < 1) {
                break;
            }
            p->foundFlag |= 0x0004 ;
            WElement2RateSet((LPSUP_RATE_ELEMENT)&pBuf[-2], &p->rateSet);
            if (((p->rateSet.Basic & ~(pWork->RateSet.Basic | pWork->RateSet.Support)) == 0) && (((p->rateSet.Basic | p->rateSet.Support) & pWork->RateSet.Basic) == pWork->RateSet.Basic)) {
                p->matchFlag |= 0x0004 ;
            } else {
                p->matchFlag &= ~0x0004 ;
            }
            break;
        case 2 :
            break;
        case 3 :
            if (len < 1) {
                break;
            }
            p->foundFlag |= 0x0002 ;
            p->channel = WL_ReadByte(&pBuf[0]);
            if (p->channel == ((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.pReq.Join->bssDesc.channel) {
                p->matchFlag |= 0x0002 ;
            } else {
                p->matchFlag &= ~0x0002 ;
            }
            break;
        case 5 :
            if (len < 3) {
                break;
            }
            p->foundFlag |= 0x0100 ;
            p->pTIM = (LPTIM_ELEMENT)&pBuf[-2];
            break;
        case 4 :
            if (len < 6) {
                break;
            }
            p->foundFlag |= 0x0200 ;
            p->pCFP = (LPCF_PARAM_ELEMENT)&pBuf[-2];
            break;
        case 6 :
            break;
        case 221 :
            if ((len < 3 + 1 + 4) || (WL_ReadByte(&pBuf[0]) != 0x00 ) || (WL_ReadByte(&pBuf[1]) != 0x09 ) || (WL_ReadByte(&pBuf[2]) != 0xBF ) || (WL_ReadByte(&pBuf[3]) != 0x00 )) {
                p->otherElementCount++;
                p->otherElementLength += (len + 2);
            } else {
                p->foundFlag |= 0x0400 ;
                p->pGMIF = (LPGAME_INFO_ELEMENT)&pBuf[-2];
            }
            break;
        default:
            p->otherElementCount++;
            p->otherElementLength += (len + 2);
        }
        pBuf += len;
        i -= (len + 2);
    }
    if (p->foundFlag & 0x0008 ) {
        if ((pWork->BSSID[0] & 0x0001) || (p->rxStatus & (0x0001 << 15) )) {
            p->matchFlag |= 0x0008 ;
        }
    }
    if (p->foundFlag & 0x0030 ) {
        if ((p->capability & ((0x01 << 0) | (0x01 << 1) )) == (pWork->CapaInfo & ((0x01 << 0) | (0x01 << 1) ))) {
            p->matchFlag |= 0x0010 ;
        }
        if ((p->capability & (0x01 << 4) ) == (pWork->CapaInfo & (0x01 << 4) )) {
            p->matchFlag |= 0x0020 ;
        }
    }
}
void RxManCtrlTask(void)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    u32 mode = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode;
    LPRXFRM pFrm;
    LPRXPACKET pPacket;
    LPMAN_HEADER pDot11Header;
    u32 cam_adrs, type, subtype;
    pPacket = (LPRXPACKET)((u32)(*(LPHEAPBUF_MAN)&pHeapMan->RxManCtrl).Head) ;
    if ((u32)pPacket == (u32)(-1) ) {
        return;
    }
    pFrm = &pPacket->frame;
    pDot11Header = (LPMAN_HEADER)&pFrm->Dot11Header;
    if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
        pCounter->rx.multicast++;
    } else {
        pCounter->rx.unicast++;
    }
    pCounter->rx.fragment += (((pFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) - 1);
    type = pDot11Header->FrameCtrl.Bit.Type;
    subtype = pDot11Header->FrameCtrl.Bit.SubType;
    cam_adrs = CAM_SearchAdd(pDot11Header->SA);
    pFrm->FirmHeader.CamAdrs = cam_adrs;
    switch (cam_adrs) {
    case 255 :
        cam_adrs = 0;
        pFrm->FirmHeader.CamAdrs = 0;
        switch (mode) {
        case 1 :
            if (type == 0x00 ) {
                switch (subtype) {
                case 0x0B :
                    RxAuthFrame((LPAUTH_FRAME)pFrm);
                    break;
                case 0x04 :
                    RxProbeReqFrame((LPPRBREQ_FRAME)pFrm);
                    break;
