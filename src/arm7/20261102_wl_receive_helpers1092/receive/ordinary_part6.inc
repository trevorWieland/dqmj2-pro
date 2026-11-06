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
static void RxPsPollFrame(LPPSPOLL_FRAME pFrm)
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
static void RxCfEndFrame(LPCFEND_FRAME pFrm)
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
    LPWL_MAN pCounterContext = (LPWL_MAN)native_host_arm7_data_0380fff4;
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
        pCounterContext->Counter.rx.multicast++;
    } else {
        pCounterContext->Counter.rx.unicast++;
    }
    pCounterContext->Counter.rx.fragment += (((pFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) - 1);
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
                case 0x00 :
                    RxAssReqFrame((LPASSREQ_FRAME)pFrm);
                    break;
                }
            }
        }
        break;
    default:
        CAM_UpdateLifeTime(cam_adrs);
        CAM_SetRSSI(cam_adrs, LoadLow(&pFrm->MacHeader.Rx.rsv_RSSI));
        if (type == 0x00 ) {
            u32 seqctrl = pFrm->Dot11Header.SeqCtrl.Data;
            if (seqctrl == CAM_GetLastSeqCtrl(cam_adrs)) {
                ;
                pCounterContext->Counter.rx.duplicateErr++;
                break;
            }
            CAM_SetLastSeqCtrl(cam_adrs, seqctrl);
        }
        switch (mode) {
        case 1 :
        {
            CAM_SetPowerMgtMode(cam_adrs, pDot11Header->FrameCtrl.Bit.PowerMan);
        }
            if (type == 0x00 ) {
                switch (subtype) {
                case 0x08 :
                    RxBeaconFrame((LPBEACON_FRAME)pFrm);
                    break;
                case 0x00 :
                    RxAssReqFrame((LPASSREQ_FRAME)pFrm);
                    break;
                case 0x02 :
                    RxReAssReqFrame((LPREASSREQ_FRAME)pFrm);
                    break;
                case 0x04 :
                    RxProbeReqFrame((LPPRBREQ_FRAME)pFrm);
                    break;
                case 0x05 :
                    RxProbeResFrame((LPPRBRES_FRAME)pFrm, 0 );
                    break;
                case 0x0A :
                    RxDisAssFrame((LPDISASS_FRAME)pFrm);
                    break;
                case 0x0B :
                    RxAuthFrame((LPAUTH_FRAME)pFrm);
                    break;
                case 0x0C :
                    RxDeAuthFrame((LPDEAUTH_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else if (type == 0x01 ) {
                switch (subtype) {
                case 0x0A :
                    RxPsPollFrame((LPPSPOLL_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else {
                ;
            }
            break;
        case 2 :
        case 3 :
            if (type == 0x00 ) {
                switch (subtype) {
                case 0x08 :
                    RxBeaconFrame((LPBEACON_FRAME)pFrm);
                    break;
                case 0x01 :
                    RxAssResFrame((LPASSRES_FRAME)pFrm);
                    break;
                case 0x03 :
                    RxReAssResFrame((LPREASSRES_FRAME)pFrm);
                    break;
                case 0x04 :
                    break;
                case 0x05 :
                    RxProbeResFrame((LPPRBRES_FRAME)pFrm, 0 );
                    break;
                case 0x0A :
                    RxDisAssFrame((LPDISASS_FRAME)pFrm);
                    break;
                case 0x0B :
                    RxAuthFrame((LPAUTH_FRAME)pFrm);
                    break;
                case 0x0C :
                    RxDeAuthFrame((LPDEAUTH_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else if (type == 0x01 ) {
                switch (subtype) {
                case 0x0E :
                case 0x0F :
                    RxCfEndFrame((LPCFEND_FRAME)pFrm);
                    break;
                default:
                    ;
                }
            } else {
                ;
            }
            break;
        }
    }
    ReleaseHeapBuf(&pHeapMan->RxManCtrl, pPacket);
    if (((*(LPHEAPBUF_MAN)&pHeapMan->RxManCtrl).Count) != 0) {
        AddTask(1 , 7 );
    }
}
static void SetChallengeText(u32 camAdrs, LPAUTH_FRAME pFrm)
{
    u32 i, txtLen;
    u16 *pText;
    u16 rnd;
    ;
    rnd = *(vu16 *)(0x04808000 + 0x044) + (*(vu16 *)(0x04808000 + 0x044) << 8);
    if (rnd == 0) {
        rnd = 1;
    }
    RND_seed(rnd);
    CAM_SetAuthSeed(camAdrs, rnd);
    pText = (u16 *)pFrm->Body.ChallengeText.Text;
    txtLen = WL_ReadByte(&pFrm->Body.ChallengeText.Length);
    for (i = 0; i < txtLen; i += 2) {
        *pText++ = RND_rand();
    }
}
static u32 CheckChallengeText(LPAUTH_FRAME pFrm)
{
    u32 i, txtLen;
    u16 *pText;
    RND_seed(CAM_GetAuthSeed(pFrm->FirmHeader.CamAdrs));
    pText = (u16 *)pFrm->Body.ChallengeText.Text;
    txtLen = WL_ReadByte(&pFrm->Body.ChallengeText.Length);
    for (i = 0; i < txtLen / 2; i++) {
        if (*pText++ != RND_rand()) {
            return 0 ;
        }
    }
    if (txtLen & 1) {
        if ((*pText & 0x00FF) != (RND_rand() & 0x00FF)) {
            return 0 ;
        }
    }
    return 1 ;
}
