u16 WSetPowerMgtMode(u32 mode)
{
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.PowerMgtMode = mode;
    if (mode && (pConfig->Mode != 1 )) {
        *(vu16 *)((0x04808000) + 0x006) |= (0x0001 << 6) ;
    } else {
        *(vu16 *)((0x04808000) + 0x006) &= ~(0x0001 << 6) ;
        WSetActiveZoneTime(pConfig->ActiveZone, 0 );
    }
    return 0;
}

u16 WSetForcePowerState(u32 state)
{
    *(vu16 *)((0x04808000) + 0x040) = (u16)state;
    return 0;
}

void WShutdown(void)
{
    u32 tmp;
    switch (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Rf.Id) {
    case 2 :
        RF_Write(0x00C008);
        break;
    }
    tmp = BBP_Read(30) | 0x3f;
    BBP_Write(30, tmp);
    *(vu16 *)(0x04808000 + 0x168) = 0x800D;
    *(vu16 *)(0x04808000 + 0x036) = 1 ;
}

void WWakeUp(void)
{
    u32 bp;
    *(vu16 *)(0x04808000 + 0x036) = 0 ;
    WWait(8);
    *(vu16 *)(0x04808000 + 0x168) = 0;
    switch (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Rf.Id) {
    case 2 :
        bp = BBP_Read(0x01);
        BBP_Write(0x01, bp & 0x7F);
        BBP_Write(0x01, bp);
        WWait(40);
        InitRF();
        break;
    case 3 :
        InitRF();
        break;
    default:
        ;
        break;
    }
}

u16 WSetFrameLifeTime(u32 lifeTimePerBeacon)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config;
    if (lifeTimePerBeacon == 0xFFFF) {
        pConfig->FrameLifeTimePerBeacon = 0xFFFF;
        pWork->FrameLifeTime = 0xFFFF;
    } else {
        u32 lifeTime = (u32)lifeTimePerBeacon * (u32)pWork->BeaconPeriod / 100 ;
        if (lifeTime > 0x00010000) {
            return 0x05 ;
        }
        pConfig->FrameLifeTimePerBeacon = lifeTimePerBeacon;
        pWork->FrameLifeTime = lifeTime;
    }
    return 0;
}

void WEnableTmpttPowerSave(void)
{
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.TmpttPs = 0;
    *(vu16 *)((0x04808000) + 0x038) |= (0x0001 << 1) ;
}

void WSetAids(u16 aid)
{
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.AID = aid;
    *(vu16 *)((0x04808000) + 0x02A) = aid;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.NullKeyRes) {
        *(vu16 *)((0x04808000) + 0x028) = aid;
    }
}

void WClearAids(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    pWork->AID = 0;
    WaitLoop_ClrAid();
    *(vu16 *)((0x04808000) + 0x02A) = 0;
    if (pWork->APCamAdrs != 0) {
        DeleteTxFrames(pWork->APCamAdrs);
        CAM_SetStaState(pWork->APCamAdrs, 0x20 );
        pWork->APCamAdrs = 0;
    }
}

void WSetStaState(u32 state)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    if (pWork->STA == state) {
        return;
    }
    if (pWork->STA == 0x40 ) {
        ClearTimeOut();
    }
    switch (state) {
    case 0x00 :
        WShutdown();
        break;
    case 0x10 :
        WSetForcePowerState((0x0000 << 15) );
        WStop();
        WWakeUp();
        break;
    case 0x40 :
        if (pWork->Mode == 2 ) {
            WEnableTmpttPowerSave();
        }
        SetupPeriodicTimeOut(100 , WIntervalTimer);
        break;
    }
    pWork->STA = state;
}

void WSetMacAdrs1(u16 *dst, u16 *src1)
{
    *dst++ = *src1++;
    *dst++ = *src1++;
    *dst = *src1;
}

void WElement2RateSet(LPSUP_RATE_ELEMENT pSup, LPRATE_SET pRateSet)
{
    u32 i, length, brate, srate;
    pRateSet->Basic = 0;
    pRateSet->Support = 0;
    length = WL_ReadByte(&pSup->Length);
    for (i = 0; i < length; i++) {
        brate = WL_ReadByte(&pSup->SupportedRate[i]);
        srate = (brate & 0x7F) - 1;
        if ((srate < sizeof(RateElement2Bit) / 2 ) && (RateElement2Bit[srate] != 0xFF)) {
            pRateSet->Support |= (0x01 << RateElement2Bit[srate]);
            if (brate & 0x80) {
                pRateSet->Basic |= (0x01 << RateElement2Bit[srate]);
            }
        } else {
            pRateSet->Support |= 0x8000;
            if (brate & 0x80) {
                pRateSet->Basic |= 0x8000;
            }
        }
    }
}

void WStop(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    ClearPeriodicTimeOut();
    ClearTimeOut();
    WSetStaState(0x20 );
    pWork->bUpdateGameInfo = 0 ;
    pWork->bSynchro = 0;
    *(vu16 *)((0x04808000) + 0x012) = 0;
    *(vu16 *)((0x04808000) + 0x004) = 0;
    *(vu16 *)((0x04808000) + 0x0EA) = 0;
    *(vu16 *)((0x04808000) + 0x0E8) = 0;
    *(vu16 *)((0x04808000) + 0x008) = 0;
    *(vu16 *)((0x04808000) + 0x00A) = 0;
    switch (pWork->Mode) {
    case 1 :
        StopBeaconFrame();
        break;
    }
    *(vu16 *)((0x04808000) + 0x0AC) = 0xFFFF ;
    *(vu16 *)((0x04808000) + 0x0B4) = 0xFFFF;
    DeleteAllTxFrames();
    ReleaseAllWlHeapBuf();
}

u32 BBP_Read(u32 adrs)
{
    *(vu16 *)(0x04808000 + 0x158) = (u16)((0x0006 * (0x0001 << 12)) | (adrs * (0x0001 << 0) ));
    WaitLoop_BbpAccess();
    return (u32)(*(vu16 *)(0x04808000 + 0x15C) );
}

u32 BBP_Write(u32 adrs, u32 data)
{
    *(vu16 *)(0x04808000 + 0x15A) = (u16)data;
    *(vu16 *)(0x04808000 + 0x158) = (u16)((0x0005 * (0x0001 << 12)) | (adrs * (0x0001 << 0) ));
    if (WaitLoop_BbpAccess()) {
        return -1;
    }
    return 0;
}

void RF_Write(u32 data)
{
    *(vu16 *)(0x04808000 + 0x17E) = (u16)data;
    *(vu16 *)(0x04808000 + 0x17C) = (u16)(data >> 16);
    WaitLoop_RfAccess();
}

void InitRF(void)
{
    u32 eep_adrs, num, reg, bytes, adrs, i, j;
    LPRF_CONFIG pRf = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Rf;
    u32 data;
    for (i = data = 0; i < sizeof(macTxRxRegAdrs) / 2; i++) {
        FLASH_Read((u32)(&((LPFLASH_TABLE)0x002a)->macTxRxRegs[i]) , 2, (u8 *)&data);
        *(vu16 *)((0x04808000) + macTxRxRegAdrs[i]) = data;
    }
    {
        reg = (0x0000 << 14) | (((u32)pRf->Bits >> 7) * (0x0001 << 8) );
        reg |= pRf->Bits & 0x7F;
        *(vu16 *)(0x04808000 + 0x184) = (u16)reg;
        eep_adrs = (u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData) ;
        bytes = (u32)(((pRf->Bits & 0x7F) + 7) / 8);
        num = pRf->InitNum;
        if (pRf->Id == 3 ) {
            FLASH_Read((u32)(&((LPFLASH_TABLE)0x002a)->rfInit_channelDependData.MM3156Tbl.init[0]) + pRf->InitNum, 1, (u8 *)&pRf->BbpCnt);
            for (i = j = 0; i < num; i++, eep_adrs++) {
                reg = 0;
                FLASH_Read(eep_adrs, 1, (u8 *)&reg);
                reg |= ((i << 8) + (5 << 16));
                RF_Write(reg);
            }
        } else {
            for (reg = 0; num > 0; num--, eep_adrs += bytes) {
                FLASH_Read(eep_adrs, bytes, (u8 *)&reg);
                RF_Write(reg);
                if (pRf->Id == 2 ) {
                    adrs = reg >> 18;
                    if (adrs == 9) {
                        pRf->BkReg = reg & ~(0x1F << 10);
                    }
                }
            }
        }
    }
}

static void TimeoutDummy(void *arg)
{
    u32 *flag = (u32 *)arg;
    *flag = 0 ;
}

void WWait(u16 ms)
{
    WWaitus(ms * 1000);
}

void WWaitus(u32 us)
{
    WaitLoop_Waitus(us, TimeoutDummy);
}

void SetupPeriodicTimeOut(u32 ms, void (*pFunc)(void *))
{
    OSTick startTime;
    OS_CancelAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->PeriodicAlarm);
    ms = ((OSTick)(((33514000 / 1000) * (u64)(ms)) / 64)) ;
    startTime = OS_GetTick() + ms;
    OS_SetPeriodicAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->PeriodicAlarm, startTime, ms, pFunc, 0 );
}

void ClearPeriodicTimeOut(void)
{
    OS_CancelAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->PeriodicAlarm);
}

void WIntervalTimer(void *arg)
{
    LPWL_MAN pWl = (LPWL_MAN)&((LPWL_MAN)native_host_arm7_data_0380fff4) ->TaskMan;
    pWl->Work.IntervalCount++;
    AddTask(1 , 10 );
    AddTask(2 , 18 );
    AddTask(1 , 17 );
    if (((*(LPHEAPBUF_MAN)&pWl->HeapMan.ToWM).Count) != 0) {
        AddTask(2 , 19 );
    }
    if (pWl->Work.FatalErr) {
        AddTask(2 , 21 );
    }
}

void SetupTimeOut(u32 ms, void (*pFunc)(void *))
{
    OS_CancelAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->Alarm);
    OS_SetAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->Alarm, ((OSTick)(((33514000 / 1000) * (u64)(ms)) / 64)) , pFunc, 0 );
}

void SetupUsTimeOut(u32 us, void (*pFunc)(void *arg))
{
    OS_CancelAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->Alarm);
    OS_SetAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->Alarm, ((OSTick)(((33514000 / 1000) * (u64)(us)) / 64 / 1000)) , pFunc, 0 );
}

void ClearTimeOut(void)
{
    OS_CancelAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->Alarm);
}

void WL_WriteByte(void *p, u8 data)
{
    { if ((u32)p & 1) *(u16 *)((u32)p - 1) = (*(u16 *)((u32)p - 1) & 0x00FF) | ( data << 8); else *(u16 *)(p) = (*(u16 *)(p) & 0xFF00) | ( data & 0x00FF); } ;
}

u8 WL_ReadByte(void *p)
{
    u16 data;
    { if ((u32)p & 1) data = (u8)(*(u16 *)((u32)p - 1) >> 8); else data = (u8)(*(u16 *)(p)); } ;
    return (u8)data;
}

void RND_init(u32 a, u32 b)
{
    LPRAND_CTRL pRand = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Rand;
    pRand->a = (u16)((a & 0xFFF8) + 5);
    pRand->b = (u16)(b | 1);
}

void TerminateWlTask(void)
{
    ;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.DiagResult |= 0x8000;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x00 ) {
        WStop();
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.State != 0x00 ) {
            ((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.State = 0x00 ;
            ((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.pCfm.Cfm->resultCode = 0x06 ;
            IssueMlmeConfirm();
        }
        WShutdown();
    }
    while (DeleteTask(3 ) != 0xFFFF ) {}
    AddTask(3 , 23 );
}
