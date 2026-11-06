{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaDataReq *pReq;
    LPPRBRES_FRAME pFrm;
    u32 ofst;
    ;
    if (!IsEnableManagement()) {
        ;
        return (0) ;
    }
    pReq = (WlMaDataReq *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, ((sizeof(WlCmdHeader)) + (sizeof(PRBRES_FRAME) + 4)) + pWork->GameInfoLength);
    if ((u32)pReq == (0) ) {
        SetFatalErr(0x0002 );
        return (LPPRBRES_FRAME)pReq;
    }
    pReq->header.code = 0xFFFF ;
    pFrm = (LPPRBRES_FRAME)&pReq->frame;
    InitManHeader((LPTXFRM)pFrm, pDA);
    pFrm->Body.BeaconInterval = pWork->BeaconPeriod;
    pFrm->Body.CapaInfo.Data = pWork->CapaInfo;
    ofst = SetSSIDElement(&pFrm->Body.Buf[0]);
    ofst += SetSupRateSet(&pFrm->Body.Buf[ofst]);
    ofst += SetDSParamSet(&pFrm->Body.Buf[ofst]);
    ofst += SetGameInfoElement(&pFrm->Body.Buf[ofst]);
    pFrm->FirmHeader.Length = ofst + 8 + 2 + 2;
    pFrm->MacHeader.Tx.MPDU = pFrm->FirmHeader.Length + sizeof(MAN_HEADER) + 4;
    pFrm->Dot11Header.FrameCtrl.Data = ((0x00 * 0x0004) | (0x05 * 0x0010)) ;
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
    pMFrm->MacHeader.Tx.Status = 0;
    pMFrm->MacHeader.Tx.Status2 = 0;
    pMFrm->MacHeader.Tx.rsv_RetryCount = 0;
    pMFrm->MacHeader.Tx.MPDU = 28 - 6 - 2;
    pMFrm->Dot11Header.FrameCtrl.Data = ((0x01 * 0x0004) | (0x0A * 0x0010)) ;
    pMFrm->Dot11Header.DurationID = 0xC000 | aid;
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
u32 SetSupRateSet(u8 *pBuf)
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
                WL_WriteByte(&pBuf[len], (native_host_arm7_table_rate_bit_027f74d0[i] | 0x80));
            } else {
                WL_WriteByte(&pBuf[len], native_host_arm7_table_rate_bit_027f74d0[i]);
            }
            len++;
        }
    }
    WL_WriteByte(&pBase[1], (len - 2));
    return len;
}
u32 SetDSParamSet(u8 *pBuf)
{
    WL_WriteByte(&pBuf[0], 3 );
    WL_WriteByte(&pBuf[1], 1);
    WL_WriteByte(&pBuf[2], ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.CurrChannel);
    return 3;
}
u32 SetGameInfoElement(u8 *pBuf)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    u32 i, j, vtsf;
    u8 *p;
    i = 0;
    WL_WriteByte(&pBuf[i], 221 );
    i++;
    WL_WriteByte(&pBuf[i], ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.GameInfoLength + 3 + 1 + 4);
    i++;
    WL_WriteByte(&pBuf[i], 0x00 );
    i++;
    WL_WriteByte(&pBuf[i], 0x09 );
    i++;
    WL_WriteByte(&pBuf[i], 0xBF );
    i++;
    WL_WriteByte(&pBuf[i], 0x00 );
    i++;
    WL_WriteByte(&pBuf[i], pConfig->ActiveZone);
    i++;
    WL_WriteByte(&pBuf[i], pConfig->ActiveZone >> 8);
    i++;
    vtsf = *(vu16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) ;
    WL_WriteByte(&pBuf[i], vtsf & 0x00FF);
    i++;
    WL_WriteByte(&pBuf[i], vtsf >> 8);
    i++;
    if (pWork->GameInfoLength != 0) {
        p = (u8 *)pWork->GameInfoAdrs;
        if (pWork->GameInfoAlign & 1) {
            p++;
        }
        for (j = 0; j < pWork->GameInfoLength; j++) {
            WL_WriteByte(&pBuf[i], WL_ReadByte(p));
            i++;
            p++;
        }
    }
    return i;
}
void InitTxCtrl(void)
{
    LPTX_CTRL pTxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    MI_CpuClear32((void *)(u32)pTxCtrl, sizeof(TX_CTRL)) ;
    pTxCtrl->Txq[0].Busy = 0 ;
    pTxCtrl->Txq[0].pFrm = (LPTXFRM)0 ;
    pTxCtrl->Txq[1].Busy = 0 ;
    pTxCtrl->Txq[1].pFrm = (LPTXFRM)0 ;
    pTxCtrl->Txq[2].Busy = 0 ;
    pTxCtrl->Txq[2].pFrm = (LPTXFRM)0 ;
    pTxCtrl->BkKeyIn = 0xFFFF;
    pTxCtrl->BkKeyOut = 0xFFFF;
    switch (pWork->Mode) {
    case 0 :
        pTxCtrl->Txq[0 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) );
        pTxCtrl->Txq[1 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) - 6 + 2)) );
        pTxCtrl->Txq[2 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + 0x0000 );
        pTxCtrl->Txq[0 ].pEndFunc = TxqEndData;
        pTxCtrl->Txq[1 ].pEndFunc = TxqEndManCtrl;
        pTxCtrl->Txq[2 ].pEndFunc = TxqEndPsPoll;
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) - 6 + 2)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) - 6 + 2)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 2) = 0x1D46 ;
        pWork->FrameCtrl = ((0x02 * 0x0004) | (0x00 * 0x0010)) ;
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 0) ;
        break;
    case 1 :
        pTxCtrl->Txq[0 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + ((((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) );
        pTxCtrl->Txq[1 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) );
        pTxCtrl->Txq[2 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) );
        pTxCtrl->Txq[0 ].pEndFunc = TxqEndData;
        pTxCtrl->Txq[1 ].pEndFunc = TxqEndManCtrl;
        pTxCtrl->Txq[2 ].pEndFunc = TxqEndBroadCast;
        pTxCtrl->Beacon.pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) );
        pTxCtrl->Mp.pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + 0x0000 );
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + ((((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + ((((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + (((((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (((((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 2) = 0x1D46 ;
        pWork->FrameCtrl = ((0x02 * 0x0004) | (0x00 * 0x0010)) | 0x0200 ;
        pTxCtrl->Beacon.pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) );
        MakeBeaconFrame();
        break;
    case 2 :
        pTxCtrl->Txq[0 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + ((((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) );
        pTxCtrl->Txq[1 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) );
        pTxCtrl->Txq[2 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) );
        pTxCtrl->Txq[0 ].pEndFunc = TxqEndData;
        pTxCtrl->Txq[1 ].pEndFunc = TxqEndManCtrl;
        pTxCtrl->Txq[2 ].pEndFunc = TxqEndPsPoll;
        pTxCtrl->Key[0].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + 0x0000 );
        pTxCtrl->Key[1].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) );
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + ((((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + ((((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + (((((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (((((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 2) = 0x1D46 ;
        pWork->FrameCtrl = ((0x02 * 0x0004) | (0x00 * 0x0010)) | 0x0100 ;
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 0) | (0x0001 << 2) | (0x0001 << 3) ;
        break;
    case 3 :
        pTxCtrl->Txq[0 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) );
        pTxCtrl->Txq[1 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) - 6 + 2)) );
        pTxCtrl->Txq[2 ].pMacFrm = (LPTXFRM_MAC)((0x04800000 + 0x4000) + 0x0000 );
        pTxCtrl->Txq[0 ].pEndFunc = TxqEndData;
        pTxCtrl->Txq[1 ].pEndFunc = TxqEndManCtrl;
        pTxCtrl->Txq[2 ].pEndFunc = TxqEndPsPoll;
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) - 6 + 2)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) - 6 + 2)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + ((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) - 2) = 0x1D46 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 4) = 0xB6B8 ;
        *(u16 *)((0x04800000 + 0x4000) + (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) - 2) = 0x1D46 ;
        pWork->FrameCtrl = ((0x02 * 0x0004) | (0x00 * 0x0010)) | 0x0100 ;
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 0) | (0x0001 << 2) | (0x0001 << 3) ;
        break;
    }
    if (pConfig->WepMode != 0 ) {
        pWork->FrameCtrl |= 0x4000 ;
    }
}
