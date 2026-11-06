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

u16 PARAMSET_AllReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_LifeTimeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt);

u16 PARAMSET_AllReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt)
{
    u16 ret;
    WlParamSetAllReq *pReq = (WlParamSetAllReq *)pReqt;
    pCfmt->header.length = 1;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x10 ) {
        return 0x01 ;
    }
    ret = WSetMacAdrs(pReq->staMacAdrs);
    ret |= WSetRetryLimit(pReq->retryLimit);
    ret |= WSetEnableChannel(pReq->enableChannel);
    ret |= WSetMode(pReq->mode);
    ret |= WSetRate(pReq->rate);
    ret |= WSetWepMode(pReq->wepMode);
    ret |= WSetWepKeyId(pReq->wepKeyId);
    ret |= WSetWepKey((u16 *)pReq->wepKey);
    ret |= WSetBeaconType(pReq->beaconType);
    ret |= WSetBcSsidResponse(pReq->probeRes);
    ret |= WSetBeaconLostThreshold(pReq->beaconLostTh);
    ret |= WSetActiveZoneTime(pReq->activeZoneTime, 0 );
    ret |= WSetSsidMask((u16 *)pReq->ssidMask);
    ret |= WSetPreambleType(pReq->preambleType);
    ret |= WSetAuthAlgo(pReq->authAlgo);
    return ret;
}

u16 PARAMSET_LifeTimeReqCmd(WlCmdReq *pReqt, WlCmdCfm *pCfmt)
{
    WlParamSetLifeTimeReq *pReq = (WlParamSetLifeTimeReq *)pReqt;
    LPCAM_ELEMENT pCAM = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM;
    u32 i;
    pCfmt->header.length = 1;
    if ((pReq->tableNumber >= ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum) && (pReq->tableNumber != 0xFFFF)) {
        return 0x05 ;
    }
    if ((pReq->frameLifeTime > 63 ) && (pReq->frameLifeTime != 0xFFFF)) {
        return 0x05 ;
    }
    if (pReq->tableNumber == 0xFFFF) {
        for (i = 1; i < ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum; i++) {
            pCAM[i].maxLifeTime = pReq->camLifeTime;
            if (pCAM[i].lifeTime != 0) {
                pCAM[i].lifeTime = pReq->camLifeTime;
            }
        }
    } else if (pReq->tableNumber != 0) {
        pCAM[pReq->tableNumber].maxLifeTime = pReq->camLifeTime;
        if (pCAM[pReq->tableNumber].lifeTime != 0) {
            pCAM[pReq->tableNumber].lifeTime = pReq->camLifeTime;
        }
    }
    if (pReq->frameLifeTime != 0) {
        WSetFrameLifeTime(pReq->frameLifeTime);
    }
    return 0x00 ;
}
