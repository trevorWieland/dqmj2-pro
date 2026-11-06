typedef struct {
    u8 *pCmd;
    u16 Busy;
    u16 pad;
} CMDIF_MAN, *LPCMDIF_MAN;

typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    DATA_HEADER Dot11Header;
    u8 Body[4];
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

void WaitLoop_Waitus(u32 us, void (*TimeoutFunc)(void *));

void WaitLoop_ClrAid(void);

u32 WaitLoop_BbpAccess(void);

u32 WaitLoop_RfAccess(void);

typedef struct {
    u8 init[2 * 5];
    u16 ch_Reg[14];
    u8 ch_PwrBB[14];
} MAX2822_TABLE, *LPMAX2822_TABLE;

typedef struct {
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

const u16 RateElement2Bit[] = {
    0xFF,
    0,
    0xFF,
    1,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    2,
    3,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    4,
    0xFF,
    0xFF,
    0xFF,
    5,
    0xFF,
    6,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    7,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    8,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    9,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    10,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    11,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
    0xFF,
};

u16 WSetMode(u16 mode)
{
    if (mode > 3 ) {
        return 0x05 ;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Mode = mode;
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Mode = mode;
    *(vu16 *)((0x04808000) + 0x006) = (u16)((*(vu16 *)((0x04808000) + 0x006) & (u16)~ (0x0007 << 0)) | ((u16) mode)) ;
    WSetPowerMgtMode(((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.PowerMgtMode);
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.ParamFlag |= (0x01UL << 3) ;
    return 0;
}

u16 WSetActiveZoneTime(u16 time, u32 update)
{
    u8 *p;
    if (time < 10 ) {
        return 0x05 ;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.ActiveZone = time;
    if (update) {
        *(vu16 *)((0x04808000) + 0x134) = time;
    }
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.Busy) {
        p = (u8 *)((u32)((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.pMacFrm->Body + ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.Ofst.Beacon.GameInfo + 2 + 3 + 1);
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.PowerMgtMode == 1 ) {
            WL_WriteByte(p++, time);
            WL_WriteByte(p, time >> 8);
        } else {
            WL_WriteByte(p++, 0xFF);
            WL_WriteByte(p, 0xFF);
        }
    }
    return 0;
}

u16 WSetMainAntenna(u32 mainAntenna)
{
    if (mainAntenna > 1 ) {
        return 0x05 ;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.MainAntenna = mainAntenna;
    *(vu16 *)(0x04808000 + 0x290) = (u16)(((LPWL_MAN)native_host_arm7_data_0380fff4)->Config.UseAntenna ^ ((LPWL_MAN)native_host_arm7_data_0380fff4)->Config.MainAntenna) ;
    return 0;
}

u16 WSetDiversity(u32 diversity, u32 useAntenna)
{
    if ((diversity > 1 ) || (useAntenna > 1 )) {
        return 0x05 ;
    }
    switch (diversity) {
    case 0 :
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.UseAntenna = useAntenna;
        break;
    case 1 :
        if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Mode != 1 ) {
            return 0x0B ;
        }
        ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.UseAntenna = 0 ;
        break;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Diversity = diversity;
    *(vu16 *)(0x04808000 + 0x290) = (u16)(((LPWL_MAN)native_host_arm7_data_0380fff4)->Config.UseAntenna ^ ((LPWL_MAN)native_host_arm7_data_0380fff4)->Config.MainAntenna) ;
    return 0;
}

u16 WSetBssid(u16 *pBssid)
{
    WSetMacAdrs1(((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BSSID, pBssid);
    WSetMacAdrs1((u16 *)((0x04808000) + 0x020) , pBssid);
    if (pBssid[0] & 0x0001) {
        *(vu16 *)((0x04808000) + 0x0D0) &= ~(0x0001 << 10) ;
    } else {
        *(vu16 *)((0x04808000) + 0x0D0) |= (0x0001 << 10) ;
    }
    return 0;
}

u16 WSetSsid(u16 length, u8 *pSsid)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    u32 i, b = 0;
    u8 *pBuf;
    if (length > 32 ) {
        return 0x05 ;
    }
    if ((pWork->STA == 0x40 ) && (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Mode == 1 )) {
        if (pWork->SSIDLength != length) {
            return 0x06 ;
        }
        if (pWork->Ofst.Beacon.SSID != 0) {
            b = 1;
        }
    }
    for (i = 0; i < length; i++) {
        WL_WriteByte(&pWork->SSID[i], WL_ReadByte(pSsid));
        pSsid++;
    }
    for (; i < 32 ; i++) {
        WL_WriteByte(&pWork->SSID[i], 0);
    }
    pWork->SSIDLength = length;
    if (b) {
        pBuf = (u8 *)((u32)((LPWL_MAN)native_host_arm7_data_0380fff4) ->TxCtrl.Beacon.pMacFrm + 12 + 24 + 2 + (u32)pWork->Ofst.Beacon.SSID);
        for (i = 0; i < length; i++) {
            WL_WriteByte(&pBuf[i], WL_ReadByte(&pWork->SSID[i]));
        }
    }
    return 0;
}

u16 WSetBeaconPeriod(u16 period)
{
    if ((period < 10 ) || (period > 1000 )) {
        return 0x05 ;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.BeaconPeriod = period;
    *(vu16 *)((0x04808000) + 0x08C) = period;
    WSetFrameLifeTime(((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.FrameLifeTimePerBeacon);
    return 0;
}

u16 WSetDTIMPeriod(u16 period)
{
    if ((period < 1 ) || (period > 255 )) {
        return 0x05 ;
    }
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.DTIMPeriod = period;
    *(vu16 *)((0x04808000) + 0x08E) = period;
    *(vu16 *)((0x04808000) + 0x088) = 0;
    return 0;
}
