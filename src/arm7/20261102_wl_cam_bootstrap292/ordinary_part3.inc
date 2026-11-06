} RXFRM, *LPRXFRM;
typedef struct {
    u16 wlRsv[(12/2) ];
    WlCmdHeader header;
    RXFRM frame;
} RXPACKET, *LPRXPACKET;
typedef struct {
    u16 DA[3];
    u16 SA[3];
    SEQ_CTRL SeqCtrl;
    u16 pad;
} DEFRAG_TBL, *LPDEFRAG_TBL;
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
u32 CAM_Search(u16 *pMacAdrs)
{
    LPCAM_ELEMENT pCAM;
    u32 pos, i;
    if (pMacAdrs[0] & 0x0001) {
        return 0;
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.Count > 1) {
        pCAM = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[1];
        for (i = 0, pos = 1; pos < ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum; pos++, pCAM++) {
            if (pCAM->state != 0x00 ) {
                if (MatchMacAdrs(pCAM->macAdrs, pMacAdrs)) {
                    return pos;
                }
                if (++i >= ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.Count) {
                    break;
                }
            }
        }
    }
    return 255 ;
}
u32 CAM_SearchAdd(u16 *pMacAdrs)
{
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    LPCAM_ELEMENT pCAM;
    u32 pos, i, free, lifeTime;
    if (pMacAdrs[0] & 0x0001) {
        return 0;
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.Count > 1) {
        pCAM = &pConfig->pCAM[1];
        for (i = free = 0, pos = 1; pos < pConfig->MaxStaNum; pos++, pCAM++) {
            if (pCAM->state != 0x00 ) {
                if (MatchMacAdrs(pCAM->macAdrs, pMacAdrs)) {
                    return pos;
                }
                if (++i >= ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.Count) {
                    break;
                }
            } else if (free == 0) {
                free = pos;
            }
        }
        if (free != 0) {
            pos = free;
        }
    } else {
        pos = 1;
    }
    if (pos >= ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MaxStaNum) {
        pCAM = &pConfig->pCAM[0];
        lifeTime = 0x010000;
        for (i = 1, pos = 0; i < pConfig->MaxStaNum; i++) {
            if ((pCAM[i].state < 0x30 ) && (pCAM[i].frameCount == 0)) {
                if (lifeTime > pCAM[i].lifeTime) {
                    lifeTime = pCAM[i].lifeTime;
                    pos = i;
                }
            }
        }
        if (pos == 0) {
            return 255 ;
        }
    }
    CAM_InitElement(pos, pMacAdrs);
    return pos;
}
void CAM_AddBcFrame(LPHEAPBUF_MAN pBufMan, void *pBuf)
{
    LPHEAPBUF_MAN pBufManBc = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TxPri[2 ];
    u32 x;
    x = OS_DisableIrqMask((1UL << 24) );
    if (((*(LPHEAPBUF_MAN)pBufManBc).Count) == 0) {
        CAM_SetTIMElementBitmap(0);
    }
    MoveHeapBuf(pBufMan, pBufManBc, pBuf);
    OS_EnableIrqMask(x);
}
void CAM_IncFrameCount(LPTXFRM pFrm)
{
    LPCAM_ELEMENT pCAM;
    u32 x, cam_adrs;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    pCAM = CAM_GetTbl(cam_adrs);
    x = OS_DisableIrqMask((1UL << 24) );
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode == 1 ) {
        if (pCAM->frameCount == 0) {
            CAM_SetTIMElementBitmap(cam_adrs);
        }
    }
    pCAM->frameCount++;
    OS_EnableIrqMask(x);
    if ((((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotSetTIM & (1 << cam_adrs)) == 0) {
        pCAM->lifeTime = pCAM->maxLifeTime;
    }
}
void CAM_DecFrameCount(LPTXFRM pFrm)
{
    LPCAM_ELEMENT pCAM;
    u32 x, cam_adrs;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    pCAM = CAM_GetTbl(cam_adrs);
    x = OS_DisableIrqMask((1UL << 24) );
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode == 1 ) {
        if (pCAM->frameCount == 1) {
            CAM_ClrTIMElementBitmap(cam_adrs);
        }
    }
    pCAM->frameCount--;
    OS_EnableIrqMask(x);
}
void CAM_SetStaState(u16 camAdrs, u16 state)
{
    u32 x;
    ;
    x = OS_DisableIrqMask((1UL << 24) );
    if (state < 0x40 ) {
        CAM_SetAwake(camAdrs);
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotClass3 |= (1 << camAdrs);
        if ((((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode == 1 ) && (CAM_GetAID(camAdrs) != 0)) {
            CAM_ReleaseAID(camAdrs);
        }
    } else {
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotClass3 &= ~(1 << camAdrs);
        if (CAM_GetPowerMgtMode(camAdrs)) {
            CAM_SetDoze(camAdrs);
        }
    }
    CAM_GetTbl(camAdrs)->state = state;
    OS_EnableIrqMask(x);
}
void CAM_SetRSSI(u16 camAdrs, u16 rssi)
{
    LPCAM_ELEMENT pCAM = CAM_GetTbl(camAdrs);
    ;
    pCAM->rssi = rssi;
}
void CAM_SetPowerMgtMode(u16 camAdrs, u16 pmtMode)
{
    LPCAM_MAN pCamMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan;
    ;
    pCamMan->PowerMgtMode = (pCamMan->PowerMgtMode & ~(1 << camAdrs)) | (pmtMode << camAdrs);
    if (pCamMan->PowerMgtMode & ~pCamMan->NotClass3) {
        *(vu16 *)((0x04808000) + 0x0AC) = (0x0001 << 3) ;
    } else {
        *(vu16 *)((0x04808000) + 0x0AE) = (0x0001 << 3) ;
    }
}
void CAM_SetDoze(u32 camAdrs)
{
    ;
    if (CAM_GetStaState(camAdrs) == 0x40 ) {
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.PowerState &= ~(1 << camAdrs);
    }
}
void CAM_SetAwake(u32 camAdrs)
{
    ;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.PowerState |= (1 << camAdrs);
}
void CAM_SetCapaInfo(u32 camAdrs, u32 capInfo)
{
    ;
    CAM_GetTbl(camAdrs)->capaInfo = capInfo;
}
void CAM_SetSupRate(u32 camAdrs, u32 SupRate)
{
    ;
    CAM_GetTbl(camAdrs)->supRateSet = SupRate;
}
void CAM_SetLastSeqCtrl(u32 camAdrs, u32 seqCtrl)
{
    ;
    CAM_GetTbl(camAdrs)->lastSeqCtrl = seqCtrl;
}
void CAM_SetAuthSeed(u32 camAdrs, u32 seed)
{
    ;
    CAM_GetTbl(camAdrs)->authSeed = seed;
}
void CAM_UpdateLifeTime(u32 camAdrs)
{
    ;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[camAdrs].lifeTime = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[camAdrs].maxLifeTime;
}
u32 CAM_AllocateAID(u16 camAdrs)
{
    LPCAM_MAN pCamMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan;
    u32 i, map, x;
    ;
    x = OS_DisableIrqMask((1UL << 24) );
    for (i = 1, map = 2; i < 16; i++, map <<= 1) {
        if ((pCamMan->UseAidMap & map) == 0) {
            pCamMan->UseAidMap |= map;
            pCamMan->ConnectSta++;
            if (pCamMan->ConnectSta == 1) {
                WEnableTmpttPowerSave();
            }
            CAM_GetTbl(camAdrs)->aid = i;
            OS_EnableIrqMask(x);
            return i;
        }
    }
    OS_EnableIrqMask(x);
    return 0;
}
void CAM_ReleaseAID(u16 camAdrs)
{
    LPWL_MAN pWlMan = (LPWL_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    u32 aid, map;
    ;
    CAM_ClrTIMElementBitmap(camAdrs);
    aid = CAM_GetAID(camAdrs);
    if (aid) {
        map = 0x0001 << aid;
        CAM_GetTbl(camAdrs)->aid = 0;
        pWlMan->CamMan.UseAidMap &= ~map;
        pWlMan->CamMan.ConnectSta--;
        if (pWlMan->CamMan.ConnectSta == 0) {
            WDisableTmpttPowerSave();
        }
    }
}
u32 CAM_GetStaState(u32 camAdrs)
{
    return CAM_GetTbl(camAdrs)->state;
}
u32 CAM_IsActive(u32 camAdrs)
{
    return (((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.PowerState >> camAdrs) & 1;
}
u32 CAM_GetPowerMgtMode(u32 camAdrs)
{
    return (((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.PowerMgtMode >> camAdrs) & 1;
}
u16 *CAM_GetMacAdrs(u32 camAdrs)
{
    return CAM_GetTbl(camAdrs)->macAdrs;
}
u32 CAM_GetAuthSeed(u32 camAdrs)
{
    return CAM_GetTbl(camAdrs)->authSeed;
}
u32 CAM_GetLastSeqCtrl(u32 camAdrs)
{
    return CAM_GetTbl(camAdrs)->lastSeqCtrl;
}
u32 CAM_GetTxRate(u32 camAdrs)
{
    if (CAM_GetTbl(camAdrs)->supRateSet & 2) {
        return 0x14 ;
    }
    return 0x0a ;
}
u32 CAM_GetAID(u32 camAdrs)
{
    return CAM_GetTbl(camAdrs)->aid;
}
u32 CAM_GetFrameCount(u32 camAdrs)
{
    return CAM_GetTbl(camAdrs)->frameCount;
}
WlStaElement *CAM_GetTbl(u32 camAdrs)
{
    return &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[camAdrs];
}
void CAM_SetTIMElementBitmap(u32 camAdrs)
{
    LPTIM_ELEMENT pTIM;
    u32 ofst, bit, tmp, x, aid;
    ;
    if (CAM_GetStaState(camAdrs) != 0x40 ) {
        return;
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotSetTIM & (1 << camAdrs)) {
        return;
    }
    pTIM = (LPTIM_ELEMENT)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + 12 + 24 + (u32)((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Ofst.Beacon.TIM);
    x = OS_DisableIrqMask((1UL << 24) );
    if (camAdrs == 0) {
        tmp = WL_ReadByte(&pTIM->BitmapCtrl) | 0x01;
        WL_WriteByte(&pTIM->BitmapCtrl, tmp);
    } else {
        aid = CAM_GetAID(camAdrs);
        ofst = aid / 8;
        bit = aid & 7;
        tmp = WL_ReadByte(&pTIM->VitrualBitmap[ofst]) | (0x01 << bit);
        WL_WriteByte(&pTIM->VitrualBitmap[ofst], tmp);
    }
    OS_EnableIrqMask(x);
}
void CAM_ClrTIMElementBitmap(u32 camAdrs)
{
    LPTIM_ELEMENT pTIM;
    u32 ofst, bit, tmp, x, aid;
    ;
    if (CAM_GetStaState(camAdrs) != 0x40 ) {
        return;
    }
    pTIM = (LPTIM_ELEMENT)((0x04800000 + 0x4000) + (0x0000 + ((8 + 12 + 24) + 2 + 2 + 2 + 516 + 2)) + 12 + 24 + (u32)((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Ofst.Beacon.TIM);
    x = OS_DisableIrqMask((1UL << 24) );
    if (camAdrs == 0) {
        tmp = WL_ReadByte(&pTIM->BitmapCtrl) & 0xFE;
        WL_WriteByte(&pTIM->BitmapCtrl, tmp);
    } else {
        aid = CAM_GetAID(camAdrs);
        ofst = aid / 8;
        bit = aid & 7;
        tmp = WL_ReadByte(&pTIM->VitrualBitmap[ofst]) & ~(0x01 << bit);
        WL_WriteByte(&pTIM->VitrualBitmap[ofst], tmp);
    }
    OS_EnableIrqMask(x);
}
void CAM_TimerTask(void)
{
    LPWL_MAN pWlMan = (LPWL_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    LPCAM_ELEMENT pCAM = &pWlMan->Config.pCAM[1];
    LPDEAUTH_FRAME pTxDeAuthFrm;
    u32 pos, i;
    u32 cnt, state;
    cnt = pWlMan->CamMan.Count;
    for (i = 0, pos = 1; pos < pWlMan->Config.MaxStaNum; pos++, pCAM++) {
        if (pCAM->state != 0x00 ) {
            if ((pCAM->lifeTime != 0) && (pCAM->lifeTime != 0xFFFF) && (--pCAM->lifeTime == 0)) {
                if (pCAM->state >= 0x20 ) {
                    state = CAM_GetStaState(pos);
                    CAM_SetStaState(pos, 0x20 );
                    DeleteTxFrames(pos);
                    if (pWlMan->Work.Mode == 1 ) {
                        if (state > 0x20 ) {
                            ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotSetTIM |= (1 << pos);
                            CAM_SetPowerMgtMode(pos, 0);
                            CAM_SetAwake(pos);
                            pTxDeAuthFrm = MakeDeAuthFrame(pCAM->macAdrs, 1 , 0 );
                            if ((u32)pTxDeAuthFrm != (0) ) {
                                pTxDeAuthFrm->FirmHeader.FrameId = 0x0001 ;
                                TxManCtrlFrame((LPTXFRM)pTxDeAuthFrm);
                                i++;
                                continue;
                            } else {
                                MLME_IssueDeAuthIndication(pCAM->macAdrs, 1 );
                            }
                        }
                    } else {
                        if (pos == pWlMan->Work.APCamAdrs) {
                            pTxDeAuthFrm = MakeDeAuthFrame(pCAM->macAdrs, 1 , 0 );
