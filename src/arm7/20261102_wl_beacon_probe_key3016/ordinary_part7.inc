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
                pCounter->rx.duplicateErr++;
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
void SetChallengeText(u32 camAdrs, LPAUTH_FRAME pFrm)
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
u32 CheckChallengeText(LPAUTH_FRAME pFrm)
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
void DefragTask(void)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    LPRXPACKET pPacket;
    LPRXFRM pFrm;
    DEFRAG_TBL defragTbl;
    u32 fc;
    pPacket = (LPRXPACKET)((u32)(*(LPHEAPBUF_MAN)&pHeapMan->Defrag).Head) ;
    if ((u32)pPacket == (u32)(-1) ) {
        return;
    }
    pFrm = &pPacket->frame;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x40 ) {
        goto defrag_task_exit;
    }
    ;
    if (pFrm->MacHeader.Rx.MPDU > 24 + 1508 ) {
        ;
        goto defrag_task_exit;
    }
    fc = pFrm->Dot11Header.FrameCtrl.Data;
    if (fc & 0x0100 ) {
        WSetMacAdrs1(defragTbl.DA, pFrm->Dot11Header.Adrs3);
        if (fc & 0x0200 ) {
            ;
            goto defrag_task_exit;
        } else {
            WSetMacAdrs1(defragTbl.SA, pFrm->Dot11Header.Adrs2);
        }
    } else {
        WSetMacAdrs1(defragTbl.DA, pFrm->Dot11Header.Adrs1);
        if (fc & 0x0200 ) {
            WSetMacAdrs1(defragTbl.SA, pFrm->Dot11Header.Adrs3);
        } else {
            WSetMacAdrs1(defragTbl.SA, pFrm->Dot11Header.Adrs2);
        }
    }
    defragTbl.SeqCtrl.Data = pFrm->Dot11Header.SeqCtrl.Data;
    if ((fc & 0x0400 ) && (pFrm->Dot11Header.SeqCtrl.Bit.FragNum == 0)) {
        NewDefragment((LPRXFRM_MAC)&pFrm->MacHeader, &defragTbl);
    } else {
        MoreDefragment((LPRXFRM_MAC)&pFrm->MacHeader, &defragTbl);
    }
defrag_task_exit:
    ReleaseHeapBuf(&pHeapMan->Defrag, pPacket);
    if (((*(LPHEAPBUF_MAN)&pHeapMan->Defrag).Count) != 0) {
        AddTask(2 , 9 );
    }
}
void NewDefragment(LPRXFRM_MAC pMFrm, LPDEFRAG_TBL pDefragTbl)
{
    LPDEFRAG_LIST pList = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl.DefragList;
    LPRXPACKET pPacket;
    LPRXFRM pFrm;
    u32 i, pos, fragCnt, SrcOfst, WSize, OvrCnt;
    ;
    pos = -1;
    for (i = 0; i < 3 ; i++) {
        if (pList[i].RestTime != 0) {
            if ((MatchMacAdrs(pList[i].DefragTbl.DA, pDefragTbl->DA)) && (MatchMacAdrs(pList[i].DefragTbl.SA, pDefragTbl->SA)) && (pList[i].DefragTbl.SeqCtrl.Bit.SeqNum == pDefragTbl->SeqCtrl.Bit.SeqNum)) {
                ;
                fragCnt = ((pMFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) ;
                OvrCnt = fragCnt - pList[i].DefragTbl.SeqCtrl.Bit.FragNum;
                if ((OvrCnt != 0) && (OvrCnt & 0x80000000) == 0) {
                    pFrm = &pList[i].pPacket->frame;
                    SrcOfst = pFrm->MacHeader.Rx.MPDU;
                    WSize = pMFrm->MacHeader.Rx.MPDU - SrcOfst - 24;
                    if ((WSize != 0) && ((WSize & 0x80000000) == 0)) {
                        MI_CpuCopy16((void *)(u32)&pMFrm->Body[SrcOfst], (void *) (u32)&pFrm->Body[pFrm->MacHeader.Rx.MPDU], WSize) ;
                        pFrm->MacHeader.Rx.MPDU += WSize;
                        pList[i].DefragTbl.SeqCtrl.Bit.FragNum = fragCnt;
                        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.rx.fragment += fragCnt;
                    }
                }
                return;
            }
        } else {
            pos = i;
        }
    }
    if (pos != -1) {
        pPacket = (LPRXPACKET)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, (sizeof(WlCmdHeader) + (8 + 12 + 24 + 1508) + 4 + sizeof(WlCmdCfm)) );
        if ((u32)pPacket != (0) ) {
            ;
            MI_CpuCopy16((void *)(u32)pDefragTbl, (void *) (u32)&pList[pos].DefragTbl, sizeof(DEFRAG_TBL)) ;
            pList[pos].RestTime = 5 ;
            pList[pos].pPacket = pPacket;
            pFrm = &pPacket->frame;
            MI_CpuCopy16((void *)(u32)pMFrm, (void *) (u32)&pFrm->MacHeader, pMFrm->MacHeader.Rx.MPDU + sizeof(MAC_HEADER)) ;
            MI_WaitDma(((LPWL_MAN)native_host_arm7_data_0380fff4)->DmaChannel) ;
            fragCnt = ((pFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) ;
            pList[pos].DefragTbl.SeqCtrl.Bit.FragNum = fragCnt;
            ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.rx.fragment += fragCnt;
            pFrm->MacHeader.Rx.MPDU = pMFrm->MacHeader.Rx.MPDU - 24;
            pList[pos].UnitLength = pFrm->MacHeader.Rx.MPDU / fragCnt;
        } else {
            SetFatalErr(0x0004 );
        }
    }
}
void MoreDefragment(LPRXFRM_MAC pMFrm, LPDEFRAG_TBL pDefragTbl)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    LPDEFRAG_LIST pList = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl.DefragList;
    LPRXFRM pFrm;
    u32 i, fragCnt, length, OvrCnt, SrcOfst, WSize;
    ;
    pMFrm->MacHeader.Rx.MPDU -= 24;
    for (i = 0; i < 3 ; i++) {
        if (pList[i].RestTime != 0) {
            if ((MatchMacAdrs(pList[i].DefragTbl.DA, pDefragTbl->DA)) && (MatchMacAdrs(pList[i].DefragTbl.SA, pDefragTbl->SA)) && (pList[i].DefragTbl.SeqCtrl.Bit.SeqNum == pDefragTbl->SeqCtrl.Bit.SeqNum)) {
                OvrCnt = pList[i].DefragTbl.SeqCtrl.Data - pDefragTbl->SeqCtrl.Data;
                if ((OvrCnt & 0x80000000) == 0) {
                    SrcOfst = OvrCnt * pList[i].UnitLength;
                    WSize = pMFrm->MacHeader.Rx.MPDU - SrcOfst;
                    if ((WSize != 0) && ((WSize & 0x80000000) == 0)) {
                        break;
                    }
                }
                return;
            }
        }
    }
    if (i != 3 ) {
        ;
        pFrm = &pList[i].pPacket->frame;
        length = pFrm->MacHeader.Rx.MPDU + WSize;
        if (length > 1508 ) {
            ;
            ReleaseHeapBuf(&pHeapMan->TmpBuf, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
            pList[i].RestTime = 0;
            return;
        }
        MI_CpuCopy16((void *)(u32)&pMFrm->Body[SrcOfst], (void *) (u32)&pFrm->Body[pFrm->MacHeader.Rx.MPDU], WSize + 1) ;
        pFrm->MacHeader.Rx.MPDU = length;
        fragCnt = ((pMFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) ;
        pList[i].DefragTbl.SeqCtrl.Bit.FragNum += (fragCnt - OvrCnt);
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter.rx.fragment += fragCnt;
        if ((pMFrm->MacHeader.Rx.Status & (0x0001 << 8) ) == 0) {
            ;
            pList[i].RestTime = 0;
            pFrm->MacHeader.Rx.Status = (pFrm->MacHeader.Rx.Status & ~(0x000F * (0x0001 << 4)) ) + (1 * (0x0001 << 4) );
            pFrm->MacHeader.Rx.MPDU += 24;
            switch (pFrm->MacHeader.Rx.Status & (0x000F) ) {
            case (0x0008 << 0) :
                MoveHeapBuf(&pHeapMan->TmpBuf, &pHeapMan->RxData, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
                AddTask(2 , 6 );
                break;
            case (0x0000 << 0) :
                MoveHeapBuf(&pHeapMan->TmpBuf, &pHeapMan->RxManCtrl, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
                AddTask(1 , 7 );
                break;
            default:
                ReleaseHeapBuf(&pHeapMan->TmpBuf, (void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) );
                break;
            }
        }
    }
}
void DefragTimerTask(void)
{
    LPDEFRAG_LIST pList = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl.DefragList;
    u32 i;
    for (i = 0; i < 3 ; i++) {
        if (pList[i].RestTime != 0) {
            if (--pList[i].RestTime == 0) {
                ;
                ReleaseHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pList[i].pPacket);
            }
        }
    }
}
void InitRxCtrl(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl;
    u32 str_madrs;
    MI_CpuClear32((void *)(u32)pRxCtrl, sizeof(RX_CTRL)) ;
    *(u16 *)((0x04808000) + 0x030) = 0x8000;
    switch (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode) {
    case 0 :
        str_madrs = (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    case 1 :
        str_madrs = (((((0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + ((8 + 12 + 24) + 208 + 0)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    case 2 :
        str_madrs = (((((0x0000 + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) + 2 + 516 + 2)) + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    case 3 :
        str_madrs = (((0x0000 + ((8 + 12 + 24) - 6 + 2)) + (((8 + 12 + 24) + 8 + 12) + 261 + 3)) + (((8 + 12 + 24) + 8 + 12) + 1508 + 0)) ;
        break;
    }
    *(vu16 *)(0x04808000 + 0x050) = (u16)((0x04800000 + 0x4000) + str_madrs);
    *(vu16 *)((0x04808000) + 0x056) = str_madrs / 2;
    *(vu16 *)(0x04808000 + 0x052) = (u16)((0x04800000 + 0x4000) + 0x1F60 );
    *(vu16 *)((0x04808000) + 0x05A) = str_madrs / 2;
    pRxCtrl->wlCurr = str_madrs / 2;
    pRxCtrl->LastMpSeq = 0xFFFF;
    pWork->Ofst.RxBuf.Size = 0x1F60 - str_madrs;
    *(vu16 *)(0x04808000 + 0x062) = (u16)((0x04800000 + 0x4000) + 0x1F60 - 2);
    *(u16 *)((0x04808000) + 0x030) = 0x8001;
    *(u16 *)((0x04808000) + 0x24C) = 0xFFFF;
    *(u16 *)((0x04808000) + 0x24C + 2) = 0xFFFF;
    *(u16 *)((0x04800000 + 0x4000) + 0x1f70) = 0xFFFF;
    *(u16 *)((0x04800000 + 0x4000) + 0x1f72) = 0xFFFF;
    *(vu16 *)((0x04800000 + 0x4000) + 0x1f7e) = 0xFFFF;
    *(vu16 *)((0x04800000 + 0x4000) + 0x1f76) = 0xFFFF;
}
