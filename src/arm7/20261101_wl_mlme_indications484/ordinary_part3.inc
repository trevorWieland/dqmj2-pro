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

void IssueMlmeConfirm(void)
{
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    LPCMDIF_MAN pCmdIf = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->CmdIf;
    pCmdIf->Busy &= ~0x01 ;
    SendMessageToWmDirect(&pHeapMan->RequestCmd, pCmdIf->pCmd);
    if (((*(LPHEAPBUF_MAN)&pHeapMan->RequestCmd).Count) != 0) {
        AddTask(2 , 11 );
    }
}

u32 MLME_IssueAssIndication(u16 *pMacAdrs, u16 aid, LPSSID_ELEMENT pSSID)
{
    WlMlmeAssInd *pInd;
    u32 i;
    pInd = (WlMlmeAssInd *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, sizeof(WlMlmeAssInd));
    if ((u32)pInd == (0) ) {
        SetFatalErr(0x0001 );
        return 0 ;
    }
    pInd->header.code = (0x0000 | 0x86) ;
    pInd->header.length = ((sizeof(WlMlmeAssInd) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) ;
    WSetMacAdrs1(pInd->peerMacAdrs, pMacAdrs);
    pInd->aid = aid & 0x0FFF;
    pInd->ssidLength = WL_ReadByte(&pSSID->Length);
    for (i = 0; i < pInd->ssidLength; i++) {
        if (i >= 32 ) {
            break;
        }
        WL_WriteByte(&pInd->ssid[i], WL_ReadByte(&pSSID->SSID[i]));
    }
    for (; i < 32 ; i++) {
        WL_WriteByte(&pInd->ssid[i], 0);
    }
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TmpBuf, pInd) ;
    return 1 ;
}

u32 MLME_IssueReAssIndication(u16 *pMacAdrs, u16 aid, LPSSID_ELEMENT pSSID)
{
    WlMlmeReAssInd *pInd;
    u32 i;
    pInd = (WlMlmeReAssInd *)AllocateHeapBuf(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, sizeof(WlMlmeReAssInd));
    if ((u32)pInd == (0) ) {
        SetFatalErr(0x0001 );
        return 0 ;
    }
    pInd->header.code = (0x0000 | 0x87) ;
    pInd->header.length = ((sizeof(WlMlmeReAssInd) - (12/2) * 2 - sizeof(WlCmdHeader) + 1) / 2) ;
    WSetMacAdrs1(pInd->peerMacAdrs, pMacAdrs);
    pInd->aid = aid;
    pInd->ssidLength = WL_ReadByte(&pSSID->Length);
    for (i = 0; i < pInd->ssidLength; i++) {
        if (i >= 32 ) {
            break;
        }
        WL_WriteByte(&pInd->ssid[i], WL_ReadByte(&pSSID->SSID[i]));
    }
    for (; i < 32 ; i++) {
        WL_WriteByte(&pInd->ssid[i], 0);
    }
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4)->HeapMan.TmpBuf, pInd) ;
    return 1 ;
}
