            CAM_SetStaState(i, 0x20 );
            ClearTxKeyData();
        }
    }
}
void DeleteAllTxFrames(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    switch (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode) {
    case 1 :
        MessageDeleteTx(0, 1 );
        MessageDeleteTx(1, 0 );
        MessageDeleteTx(2, 1 );
        if (pTxCtrl->Mp.Busy) {
            ;
            pTxCtrl->Mp.Busy = 0;
            pTxCtrl->Mp.InCount--;
            ReleaseHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pTxCtrl->pMpEndInd);
        }
        break;
    case 2 :
    case 3 :
        MessageDeleteTx(0, 1 );
        MessageDeleteTx(1, 0 );
        MessageDeleteTx(2, 0 );
        break;
    default:
        MessageDeleteTx(0, 0 );
        MessageDeleteTx(1, 0 );
        MessageDeleteTx(2, 0 );
        break;
    }
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
    LPTXQ pTxq = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon;
    *(vu16 *)((0x04808000) + 0x080) = 0;
    pTxq->Busy = 0 ;
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
        pWork->Ofst.Beacon.SSID = 0;
    }
    pBuf += SetSupRateSet(pBuf);
    WL_WriteByte(pBuf++, 3 );
    WL_WriteByte(pBuf++, 1);
    WL_WriteByte(pBuf++, pWork->CurrChannel);
    pWork->Ofst.Beacon.TIM = (u16)((u32)pBuf - (u32)pBody);
    *(u16 *)((0x04808000) + 0x084) = pWork->Ofst.Beacon.TIM + 2;
    WL_WriteByte(pBuf++, 5 );
    WL_WriteByte(pBuf++, 3 + 2);
    WL_WriteByte(pBuf++, 0);
    WL_WriteByte(pBuf++, pWork->DTIMPeriod);
    WL_WriteByte(pBuf++, 0);
    WL_WriteByte(pBuf++, 0);
    WL_WriteByte(pBuf++, 0);
    pWork->Ofst.Beacon.GameInfo = (u16)((u32)pBuf - (u32)pBody);
    pWork->GameInfoAlign = pWork->Ofst.Beacon.GameInfo & 1;
    WL_WriteByte(pBuf++, 221 );
    WL_WriteByte(pBuf++, 3 + 1 + 4 + pWork->GameInfoLength);
    WL_WriteByte(pBuf++, 0x00 );
    WL_WriteByte(pBuf++, 0x09 );
    WL_WriteByte(pBuf++, 0xBF );
    WL_WriteByte(pBuf++, 0x00 );
    if (pWork->PowerMgtMode == 1 ) {
        WL_WriteByte(pBuf++, pConfig->ActiveZone);
        WL_WriteByte(pBuf++, (pConfig->ActiveZone >> 8));
    } else {
        WL_WriteByte(pBuf++, 0xFF);
        WL_WriteByte(pBuf++, 0xFF);
    }
    vtsf = *(u16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) ;
    WL_WriteByte(pBuf++, vtsf & 0x00FF);
    WL_WriteByte(pBuf++, vtsf >> 8);
    p = (u8 *)pWork->GameInfoAdrs;
    for (i = 0; i < pWork->GameInfoLength; i++) {
        WL_WriteByte(pBuf++, WL_ReadByte(p));
        p++;
    }
    if (pWork->GameInfoAlign) {
        p = (u8 *)((u32)pWork->GameInfoAdrs + pWork->GameInfoLength - 1);
        for (i = 0; i < pWork->GameInfoLength; i++, p--) {
            WL_WriteByte(p + 1, WL_ReadByte(p));
        }
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000004 ) {
        u16 *pId = (u16 *)(((u32)pBuf + 3) & 0xFFFFFFFC);
        pId[0] = 0xB6B8 ;
        pId[1] = 0x1D46 ;
    }
    pWork->bUpdateGameInfo = 0 ;
    pFrm->MacHeader.Tx.MPDU = 24 + (u32)pBuf - (u32)pBody + 4;
}
void UpdateGameInfoElement(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPGAME_INFO_ELEMENT pGMIF = (LPGAME_INFO_ELEMENT)((u32)((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.pMacFrm->Body + pWork->Ofst.Beacon.GameInfo);
    if (pWork->GameInfoLength != 0) {
        if ((u32)pWork->GameInfoAlign & 1) {
            DMA_Write((void *)((u32)pGMIF->GameInfo - 1), pWork->GameInfoAdrs, pWork->GameInfoLength + 2);
            WL_WriteByte(&pGMIF->VTSF[1], *(vu16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) >> 8);
        } else {
            DMA_Write(pGMIF->GameInfo, pWork->GameInfoAdrs, pWork->GameInfoLength + 1);
        }
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.pMacFrm->MacHeader.Tx.MPDU = 24 + pWork->Ofst.Beacon.GameInfo + 2 + 3 + 1 + 4 + pWork->GameInfoLength + 4;
    WL_WriteByte(&pGMIF->Length, 3 + 1 + 4 + pWork->GameInfoLength);
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->WlOperation & 0x00000004 ) {
        u16 *pId = (u16 *)(((u32)pGMIF + 1 + 1 + 3 + 1 + 4 + pWork->GameInfoLength + 3) & 0xFFFFFFFC);
        pId[0] = 0xB6B8 ;
        pId[1] = 0x1D46 ;
    }
    pWork->bUpdateGameInfo = 0 ;
}
u32 IsEnableManagement(void)
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
LPASSRES_FRAME MakeAssResFrame(u16 camAdrs, u16 statusCode, LPSSID_ELEMENT pSSID)
{
    WlMaDataReq *pReq;
    LPASSRES_FRAME pFrm;
    u32 ofst, i, aid;
    u8 *p;
    ;
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(ASSRES_FRAME) + 4)) + 34);
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPASSRES_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPASSRES_FRAME)&pReq->frame;
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
    pFrm->Body.AID = aid;
    if (aid) {
        pFrm->Body.AID |= 0xC000;
    }
    ofst = SetSupRateSet(&pFrm->Body.Buf[0]);
    pFrm->FirmHeader.Length = ofst + 2 + 2 + 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x01 * 0x0010)) ;
    p = (u8 *)((u32)&pFrm->Dot11Header + pFrm->MacHeader.Tx.MPDU);
    if (pSSID != 0 ) {
        u32 len = WL_ReadByte(&pSSID->Length);
        WL_WriteByte(p++, WL_ReadByte(&pSSID->ID));
        WL_WriteByte(p++, len);
        for (i = 0; i < len; i++, p++) {
            WL_WriteByte(p, WL_ReadByte(&pSSID->SSID[i]));
        }
    } else {
        WL_WriteByte(p++, 0 );
        WL_WriteByte(p, 0);
    }
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
LPPRBRES_FRAME MakeProbeResFrame(u16 *pDA)
