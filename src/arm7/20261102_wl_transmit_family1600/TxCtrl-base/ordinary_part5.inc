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

static u32 IsEnableManagement(void)
{
    if (((*(LPHEAPBUF_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TxPri[1]).Count) < (24 - ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.ConnectSta)) {
        return 1 ;
    }
    ;
    return 0 ;
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

void InitManHeader(LPTXFRM pFrm, u16 *pDA)
{
    MI_CpuClear16(pFrm, (sizeof(FIRM_HEADER) + sizeof(MAC_HEADER) + sizeof(MAN_HEADER)) );
    pFrm->MacHeader.Tx.Service_Rate = WCalcManRate();
    WSetMacAdrs3(pFrm->Dot11Header.Adrs1, pDA, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MacAdrs, ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID);
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
