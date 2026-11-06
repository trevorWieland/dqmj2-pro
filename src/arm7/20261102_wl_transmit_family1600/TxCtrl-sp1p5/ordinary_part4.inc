}

void MessageDeleteTx(u32 pri, u32 bMsg)
{
    WlMaDataReq *pReq, *pNextReq;
    LPTXFRM pFrm;
    pReq = (WlMaDataReq *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[pri]).Head) ;
    if ((u32)pReq == (u32)(-1) ) {
        return;
    }
    do {
        pNextReq = (WlMaDataReq *)GetHeapBufNextAdrs(pReq);
        pFrm = (LPTXFRM)&pReq->frame;
        if (pri != 2 ) {
            CAM_DecFrameCount(pFrm);
        }
        pFrm->MacHeader.Tx.Status = 2;
        if (bMsg) {
            IssueMaDataConfirm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[pri], pReq);
        }
        pReq = pNextReq;
    } while ((u32)pReq != (u32)(-1) );
}

void TxPsPollFrame(void)
{
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[2 ];
    pTxq->InCount++;
    ;
    if (pTxq->Busy) {
        pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount = 0;
    } else {
        pTxq->Busy = 1 ;
        pTxq->pMacFrm->MacHeader.Tx.Status = 0;
        pTxq->pMacFrm->MacHeader.Tx.rsv_RetryCount = 0;
        pTxq->pMacFrm->MacHeader.Tx.Service_Rate = WCalcManRate();
        *(vu16 *)(((0x04808000) + 0x0A0) + 2 * 4) = (0x0001 << 15) | (u16)(((u32)(pTxq->pMacFrm) & 0x3FFF) / 2) ;
    }
}

void StartBeaconFrame(void)
{
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon;
    pTxq->Busy = 1 ;
    *(vu16 *)((0x04808000) + 0x080) = (0x0001 << 15) | (((u32)(pTxq->pMacFrm) & 0x3FFF) / 2) ;
}

void StopBeaconFrame(void)
{
    LPWL_MAN manager = (LPWL_MAN)native_host_arm7_data_0380fff4;
    *(vu16 *)0x04808080 = 0;
    manager->TxCtrl.Beacon.Busy = 0;
}

static u32 IsEnableManagement(void)
{
    if (((*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[1]).Count) < (24 - ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.ConnectSta)) {
        return 1 ;
    }
    ;
    return 0 ;
}

LPDISASS_FRAME MakeDisAssFrame(u16 *pDA, u16 reasonCode)
{
    WlMaDataReq *pReq;
    LPDISASS_FRAME pFrm;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(DISASS_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPDISASS_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPDISASS_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.ReasonCode = reasonCode;
    pFrm->FirmHeader.Length = 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x0A * 0x0010)) ;
    return pFrm;
}

LPASSREQ_FRAME MakeAssReqFrame(u16 *pDA)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaDataReq *pReq;
    LPASSREQ_FRAME pFrm;
    u32 ofst;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(ASSREQ_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPASSREQ_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPASSREQ_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.CapaInfo.Data = pWork->CapaInfo;
    pFrm->Body.ListenInterval = pWork->ListenInterval;
    ofst = SetSSIDElement(&pFrm->Body.Buf[0]);
    ofst += SetSupRateSet(&pFrm->Body.Buf[ofst]);
    pFrm->FirmHeader.Length = ofst + 2 + 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x00 * 0x0010)) ;
    return pFrm;
}

LPREASSREQ_FRAME MakeReAssReqFrame(u16 *pDA)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaDataReq *pReq;
    LPREASSREQ_FRAME pFrm;
    u32 ofst;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(REASSREQ_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPREASSREQ_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPREASSREQ_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.CapaInfo.Data = pWork->CapaInfo;
    pFrm->Body.ListenInterval = pWork->ListenInterval;
    WSetMacAdrs1(pFrm->Body.CurrAPMacAdrs, pWork->LinkAdrs);
    ofst = SetSSIDElement(&pFrm->Body.Buf[0]);
    ofst += SetSupRateSet(&pFrm->Body.Buf[ofst]);
    pFrm->FirmHeader.Length = ofst + 2 + 2 + 6;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x02 * 0x0010)) ;
    return pFrm;
}
LPREASSRES_FRAME MakeReAssResFrame(u16 camAdrs, u16 statusCode, LPSSID_ELEMENT pSSID)
{
    WlMaDataReq *pReq;
    LPREASSRES_FRAME pFrm;
    u32 ofst, i, aid;
    u8 *p;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(ASSRES_FRAME) + 4)) + 34);
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPREASSRES_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPREASSRES_FRAME)&pReq->frame;
    if (statusCode == 0 ) {
        aid = CAM_AllocateAID(camAdrs);
        if (aid == 0) {
            statusCode = 19 ;
        }
    } else {
        aid = 0;
    }
    InitManHeader((LPTXFRM)pFrm, CAM_GetMacAdrs(camAdrs));
    pFrm->Body.CapaInfo.Data = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.CapaInfo;
    pFrm->Body.StatusCode = statusCode;
    pFrm->Body.AID = aid | 0xC000;
    ofst = SetSupRateSet(&pFrm->Body.Buf[0]);
    pFrm->FirmHeader.Length = ofst + 2 + 2 + 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x03 * 0x0010)) ;
    p = (u8 *)((u32)&pFrm->Dot11Header + pFrm->MacHeader.Tx.MPDU);
    if (pSSID != 0 ) {
        u32 len = WL_ReadByte(&pSSID->Length);
        WL_WriteByte(p, WL_ReadByte(&pSSID->ID));
        p++;
        WL_WriteByte(p, len);
        p++;
        for (i = 0; i < len; i++) {
            WL_WriteByte(p, WL_ReadByte(&pSSID->SSID[i]));
            p++;
        }
    } else {
        WL_WriteByte(p, 0 );
        p++;
        WL_WriteByte(p, 0);
    }
    return pFrm;
}

LPPRBREQ_FRAME MakeProbeReqFrame(u16 *pDA)
{
    WlMaDataReq *pReq;
    LPPRBREQ_FRAME pFrm;
    u32 ofst;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(PRBREQ_FRAME) + 4)) );
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPPRBREQ_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPPRBREQ_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    ofst = SetSSIDElement(&pFrm->Body.Buf[0]);
    ofst += SetSupRateSet(&pFrm->Body.Buf[ofst]);
    pFrm->FirmHeader.Length = ofst;
    pFrm->MacHeader.Tx.MPDU = ofst + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x04 * 0x0010)) ;
    return pFrm;
}

LPAUTH_FRAME MakeAuthFrame(u16 *pDA, u16 txtLen, u32 bCheck)
{
    WlMaDataReq *pReq;
    LPAUTH_FRAME pFrm;
    ;
    if (bCheck && !IsEnableManagement()) {
        ;
        return (0) ;
    }
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(AUTH_FRAME) - sizeof(CHALLENGE_ELEMENT) + 4)) + txtLen + 2);
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPAUTH_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPAUTH_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    if (txtLen != 0) {
        WL_WriteByte(&pFrm->Body.ChallengeText.ID, 16 );
        WL_WriteByte(&pFrm->Body.ChallengeText.Length, txtLen);
        txtLen += 2;
    }
    pFrm->FirmHeader.Length = 2 + 2 + 2 + txtLen;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x0B * 0x0010)) ;
    return pFrm;
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

void MakePsPollFrame(u16 aid)
{
    LPTXFRM_MAC pMFrm = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Txq[2 ].pMacFrm;
    ;
    u32 duration = (u32)aid | 0xC000;
    pMFrm->MacHeader.Tx.Status = 0;
    pMFrm->MacHeader.Tx.Status2 = 0;
    pMFrm->MacHeader.Tx.rsv_RetryCount = 0;
    pMFrm->MacHeader.Tx.MPDU = 28 - 6 - 2;
    pMFrm->Dot11Header.FrameCtrl.Data = ((0x01 * 0x0004) | (0x0A * 0x0010)) ;
    pMFrm->Dot11Header.DurationID = duration;
    WSetMacAdrs2(pMFrm->Dot11Header.Adrs1, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MacAdrs);
}

void InitManHeader(LPTXFRM pFrm, u16 *pDA)
{
    MI_CpuClear16(pFrm, (sizeof(FIRM_HEADER) + sizeof(MAC_HEADER) + sizeof(MAN_HEADER)) );
    pFrm->MacHeader.Tx.Service_Rate = WCalcManRate();
    WSetMacAdrs3(pFrm->Dot11Header.Adrs1, pDA, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MacAdrs, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID);
}

u32 IsExistManFrame(u16 *pDA, u16 frameCtrl)
{
    WlMaDataReq *pReq;
    LPTXFRM pFrm;
    pReq = (WlMaDataReq *)((u32)(*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[1]).Head) ;
    while ((u32)pReq != (u32)(-1) ) {
        pFrm = (LPTXFRM)&pReq->frame;
        if ((pFrm->Dot11Header.FrameCtrl.Data == frameCtrl) && MatchMacAdrs(pFrm->Dot11Header.Adrs1, pDA)) {
            ;
            return 1 ;
        }
        pReq = (WlMaDataReq *)GetHeapBufNextAdrs(pReq);
    }
    return 0 ;
}

u32 SetSSIDElement(u8 *pBuf)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    u32 len = 0, ssid_len = pWork->SSIDLength;
    u32 i;
    WL_WriteByte(&pBuf[len], 0 );
    len++;
    WL_WriteByte(&pBuf[len], ssid_len);
    len++;
    for (i = 0; i < ssid_len; i++) {
        WL_WriteByte(&pBuf[len], WL_ReadByte(&pWork->SSID[i]));
        len++;
    }
    return len;
}

static u32 SetSupRateSet(u8 *pBuf)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    u8 *pBase = pBuf;
    u32 len = 0;
    u32 i;
    WL_WriteByte(&pBuf[0], 1 );
    len++;
    len++;
    for (i = 0; i < sizeof(pWork->RateSet.Basic) * 8; i++) {
        if (pWork->RateSet.Support & (0x01 << i)) {
            if (pWork->RateSet.Basic & (0x01 << i)) {
                WL_WriteByte(&pBuf[len], (RateBit2Element[i] | 0x80));
            } else {
                WL_WriteByte(&pBuf[len], RateBit2Element[i]);
            }
            len++;
        }
    }
    WL_WriteByte(&pBase[1], (len - 2));
    return len;
}
