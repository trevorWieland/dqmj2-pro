typedef struct {
    u16 RestTime;
    u16 UnitLength;
    DEFRAG_TBL DefragTbl;
    LPRXPACKET pPacket;
} DEFRAG_LIST, *LPDEFRAG_LIST;

typedef struct {
    u16 LastMpSeq;
    u16 IcvOkCntFlag;
    u16 wlCurr;
    u16 TxKeyReg;
    DEFRAG_LIST DefragList[3 ];
} RX_CTRL, *LPRX_CTRL;

u32 RxMpFrame(LPRXFRM pFrm);

u32 RxMpAckFrame(LPRXFRM pFrm);

typedef WlApElement AP_LIST;

typedef struct {
    TASK_MAN TaskMan;
    HEAP_MAN HeapMan;
    AP_LIST ApList[4 ];
    OSMessageQueue *pSendMsgQueue;
    OSMessageQueue *pRecvMsgQueue;
    u32 DmaChannel;
    u32 DmaMaxCount;
    s32 lockID;
    void *pFlashImg;
    CONFIG_PARAM Config;
    WORK_PARAM Work;
    MLME_MAN MLME;
    CMDIF_MAN CmdIf;
    TX_CTRL TxCtrl;
    RX_CTRL RxCtrl;
    CAM_MAN CamMan;
    WlCounter Counter;
    RAND_CTRL Rand;
    RF_CONFIG Rf;
    OSAlarm PeriodicAlarm;
    OSAlarm Alarm;
    OSAlarm KeyAlarm;
    u32 WlDbgLevel;
    u16 WlOperation;
    u16 EnableChannel;
} WL_MAN, *LPWL_MAN;

u32 RxMpFrame(LPRXFRM pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPRX_CTRL pRxCtrl = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl;
    WlMaMpInd *pInd;
    u32 cnt;
    u16 bitmap, out;
    if (pWork->STA != 0x40 ) {
        return 1;
    }
    if ((MatchMacAdrs(pFrm->Dot11Header.Adrs2, pWork->BSSID) == 0) || (MatchMacAdrs(pFrm->Dot11Header.Adrs3, pWork->LinkAdrs) == 0)) {
        return 1;
    }
    ;
    ;
    bitmap = 0x0001U << pWork->AID;
    if ((bitmap & ((WlRxMpFrame *)pFrm)->bitmap) == 0) {
        ;
        pRxCtrl->TxKeyReg = 0;
        ;
    } else {
        pRxCtrl->TxKeyReg = (0x0001 << 13) ;
    }
    out = *(vu16 *)((0x04808000) + 0x098) ;
    if ((out & 0x8000) && (((LPRXFRM_MAC)((0x04800000 + 0x4000) + ((u32)(out & 0x7FFF) * 2)) )->MacHeader.Tx.rsv_RetryCount != 0)) {
        pRxCtrl->TxKeyReg |= (0x0001 << 14) ;
    }
    CAM_UpdateLifeTime(pWork->APCamAdrs);
    pFrm->FirmHeader.Length = pFrm->MacHeader.Rx.MPDU - 24 - 2 - 2;
    pInd = (WlMaMpInd *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    pInd->header.code = (0x0100 | 0x82) ;
    pInd->header.length = ((pFrm->FirmHeader.Length + sizeof(WlRxMpFrame) - 2+1)/2) ;
    bitmap = pInd->frame.bitmap;
    for (cnt = 0; bitmap != 0; bitmap >>= 1) {
        if (bitmap & 1) {
            cnt++;
        }
    }
    pInd->frame.txKeySts |= (pRxCtrl->TxKeyReg | ((*(vu16 *)((0x04808000) + 0x098) & 0x8000) >> 4) | ((*(vu16 *)((0x04808000) + 0x094) & 0x8000) >> 3));
    pInd->frame.ackTimeStamp = pInd->frame.timeStamp + ((cnt * (pInd->frame.txop + 10) + (10 + 96 + 32 * 4 + 3 + 15)) >> 4);
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pInd);
    ;
    return 0;
}

u32 RxMpAckFrame(LPRXFRM pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaMpAckInd *pInd;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x40 ) {
        return 1;
    }
    if ((MatchMacAdrs(pFrm->Dot11Header.Adrs2, pWork->BSSID) == 0) || (MatchMacAdrs(pFrm->Dot11Header.Adrs3, pWork->LinkAdrs) == 0)) {
        ;
        return 1;
    }
    ;
    pFrm->FirmHeader.Length = pFrm->MacHeader.Rx.MPDU - 24 - 2 - 2;
    pInd = (WlMaMpAckInd *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    pInd->header.code = (0x0100 | 0x85) ;
    pInd->header.length = ((sizeof(WlRxMpAckFrame)+1)/2) ;
    pInd->ack.txKeySts |= (((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl.TxKeyReg | ((*(vu16 *)((0x04808000) + 0x098) & 0x8000) >> 4) | ((*(vu16 *)((0x04808000) + 0x094) & 0x8000) >> 3));
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pInd);
    ;
    return 0;
}
