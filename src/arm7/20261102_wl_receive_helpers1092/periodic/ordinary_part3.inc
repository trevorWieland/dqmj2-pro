    u8 init[3 * 12];
    u8 ch_Reg[14][6];
    u8 ch_PwrBB[14];
    u8 ch_PwrRF[14];
} RF2958_TABLE, *LPRF2958_TABLE;
typedef struct {
    u8 init[27];
    u8 ch_BbpCnt;
    u8 ch_BB[2][15];
    u8 ch_RF[3][15];
} MM3156_TABLE, *LPMM3156_TABLE;
typedef struct {
    u8 init[29];
    u8 ch_BbpCnt;
    u8 ch_BB[2][15];
    u8 ch_RF[2][15];
} MM3156ES3_TABLE, *LPMM3156ES3_TABLE;
typedef struct {
    u8 init[29 ];
    u8 ch_BbpCnt;
    u8 ch_BB[2][15];
    u8 ch_RF[2 ][15];
} MM3156CS1_TABLE, *LPMM3156CS1_TABLE;
typedef struct {
    u8 init[32 ];
    u8 ch_BbpCnt;
    u8 ch_BB[2][15];
    u8 ch_RF[2 ][15];
} MM3156CS2_TABLE, *LPMM3156CS2_TABLE;
typedef struct {
    u8 init[41];
    u8 ch_BbpCnt;
    u8 ch_BB[2][15];
    u8 ch_RF[3][15];
} MM3218_TABLE, *LPMM3218_TABLE;
typedef struct {
    u8 init[41];
    u8 ch_BbpCnt;
    u8 ch_BB[2][15];
    u8 ch_RF[3][15];
} MM3218CS2_TABLE, *LPMM3218CS2_TABLE;
typedef struct {
    u16 checkSum;
    u16 tableSize;
    u8 vendorID;
    u8 moduleID;
    u8 serialNum[5];
    u8 rsv;
    u16 macAdrs[3];
    u16 enableChannel;
    u16 wlOperation;
    u8 rfDeviceId;
    u8 rfBitWidth;
    u8 rfInitRegNum;
    u8 rfDepChRegNum;
    u16 macTxRxRegs[16];
    u8 bbpInitRegs[105];
    u8 pad;
    union {
        MAX2822_TABLE MAX2822Tbl;
        RF2958_TABLE RF2958Tbl;
        MM3156_TABLE MM3156Tbl;
        MM3156ES3_TABLE MM3156ES3Tbl;
        MM3156CS1_TABLE MM3156CS1Tbl;
        MM3156CS2_TABLE MM3156CS2Tbl;
        MM3218_TABLE MM3218Tbl;
        MM3218CS2_TABLE MM3218CS2Tbl;
    } rfInit_channelDependData;
} FLASH_TABLE, *LPFLASH_TABLE;
void FLASH_Read(u32 adrs, u32 size, u8 *pBuf);
    const u16 macTxRxRegAdrs[16]
    = {
          0x146 ,
          0x148 ,
          0x14A ,
          0x14C ,
          0x120 ,
          0x122 ,
          0x154 ,
          0x144 ,
          0x132 ,
          0x132 ,
          0x140 ,
          0x142 ,
          0x038 ,
          0x124 ,
          0x128 ,
          0x150 ,
      };
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
void WEnableTmpttPowerSave(void)
{
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.TmpttPs = 0;
    *(vu16 *)((0x04808000) + 0x038) |= (0x0001 << 1) ;
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
void ClearTimeOut(void)
{
    OS_CancelAlarm(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->Alarm);
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
