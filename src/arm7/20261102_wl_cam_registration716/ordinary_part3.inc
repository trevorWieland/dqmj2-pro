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
u32 CAM_GetPowerMgtMode(u32 camAdrs)
{
    return (((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.PowerMgtMode >> camAdrs) & 1;
}
u32 CAM_GetAID(u32 camAdrs)
{
    return CAM_GetTbl(camAdrs)->aid;
}
WlStaElement *CAM_GetTbl(u32 camAdrs)
{
    return &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[camAdrs];
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
void CAM_InitElement(u32 camAdrs, u16 *pMacAdrs)
{
    LPCAM_ELEMENT pCAM = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.pCAM[camAdrs];
    ;
    if (pCAM->state == 0x00 ) {
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.Count++;
    }
    MI_CpuClear16((void *)(u32)pCAM, sizeof(CAM_ELEMENT) - 2) ;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->CamMan.NotSetTIM &= ~(1 << camAdrs);
    CAM_SetPowerMgtMode(camAdrs, 0);
    CAM_SetAwake(camAdrs);
    WSetMacAdrs1(pCAM->macAdrs, pMacAdrs);
    pCAM->lastSeqCtrl = 0xFFFF;
    pCAM->supRateSet = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.RateSet.Support;
    pCAM->lifeTime = pCAM->maxLifeTime;
    CAM_SetStaState(camAdrs, 0x20 );
}
