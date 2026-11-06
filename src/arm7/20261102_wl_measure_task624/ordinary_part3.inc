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
u32 FLASH_VerifyCheckSum(u32 *pCrc);
void MLME_ScanTask(void)
{
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    void *pFrm;
    u32 bTask;
    u16 ch;
    bTask = 0 ;
    switch (pMLME->State) {
    case (0x00 | 0x10) :
        WSetStaState(0x20 );
        pWork->Mode = 2 ;
        pMLME->pCfm.Scan->bssDescCount = 0;
        pMLME->pCfm.Scan->foundMap = 0;
        pMLME->Work.Scan.ChannelCount = 0;
        pMLME->Work.Scan.bFound = 0;
        if (pMLME->pReq.Scan->scanType == 0 ) {
            pMLME->Work.Scan.TxPeriod = (pMLME->pReq.Scan->maxChannelTime + 3) / 4;
            if (pMLME->Work.Scan.TxPeriod < 10 ) {
                pMLME->Work.Scan.TxPeriod = 10 ;
            }
        } else {
            pMLME->Work.Scan.TxPeriod = pMLME->pReq.Scan->maxChannelTime;
        }
        pMLME->pCfm.Scan->resultCode = 0x00 ;
    case (0x01 | 0x10) :
        ch = WL_ReadByte(&pMLME->pReq.Scan->channelList[pMLME->Work.Scan.ChannelCount]);
        if (ch == 0) {
            pMLME->State = (0x05 | 0x10) ;
            bTask = 1 ;
            break;
        }
        pMLME->Work.Scan.ChannelCount++;
        pMLME->Work.Scan.ElapseTime = 0;
        if (FLASH_VerifyCheckSum(0 ) != 0) {
            pMLME->pCfm.Scan->resultCode = 0x0E ;
            pMLME->State = (0x05 | 0x10) ;
            bTask = 1 ;
            break;
        }
        if (pMLME->State == (0x00 | 0x10) ) {
            WSetChannel(ch, 0 );
            WStart();
        } else {
            WSetChannel(ch, 0 );
        }
        pMLME->State = (0x02 | 0x10) ;
    case (0x02 | 0x10) :
    case (0x03 | 0x10) :
        pMLME->State = (0x03 | 0x10) ;
        if (pMLME->pReq.Scan->scanType == 0 ) {
            pFrm = MakeProbeReqFrame(pMLME->pReq.Scan->bssid);
            if ((u32)pFrm == (0) ) {
                pMLME->pCfm.Scan->resultCode = 0x08 ;
                pMLME->State = (0x05 | 0x10) ;
                bTask = 1 ;
                break;
            }
            TxManCtrlFrame((LPTXFRM)pFrm);
        }
        SetupTimeOut(pMLME->Work.Scan.TxPeriod, MLME_ScanTimeOut);
        break;
    case (0x05 | 0x10) :
        pMLME->State = 0x00 ;
        WStop();
        pWork->Mode = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Mode;
        IssueMlmeConfirm();
        break;
    }
    if (bTask) {
        AddTask(2 , 0 );
    }
}
void MLME_ScanTimeOut(void *arg)
{
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    pMLME->Work.Scan.ElapseTime += pMLME->Work.Scan.TxPeriod;
    if (pMLME->Work.Scan.ElapseTime >= pMLME->pReq.Scan->maxChannelTime) {
        if (pMLME->Work.Scan.ChannelCount < 16) {
            pMLME->State = (0x01 | 0x10) ;
        } else {
            pMLME->State = (0x05 | 0x10) ;
        }
    } else {
    }
    AddTask(2 , 0 );
}
void MLME_JoinTask(void)
{
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    switch (pMLME->State) {
    case (0x00 | 0x20) :
        WStart();
        pMLME->Work.Join.Result = 0 ;
        pMLME->Work.Join.Status = 0 ;
        pMLME->State = (0x01 | 0x20) ;
        SetupTimeOut(pMLME->pReq.Join->timeOut, MLME_JoinTimeOut);
        break;
    case (0x05 | 0x20) :
        ;
        ;
        pMLME->pCfm.Join->resultCode = pMLME->Work.Join.Result;
        pMLME->pCfm.Join->statusCode = pMLME->Work.Join.Status;
        if (pMLME->Work.Join.Result != 0x00 ) {
            WStop();
        }
        pMLME->State = 0x00 ;
        IssueMlmeConfirm();
        break;
    }
}
void MLME_JoinTimeOut(void *arg)
{
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    pMLME->Work.Join.Result = 0x07 ;
    pMLME->State = (0x05 | 0x20) ;
    AddTask(2 , 1 );
}
void MLME_MeasChannelTask(void)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME;
    u32 ch, ratio;
    switch (pMLME->State) {
    case (0x00 | 0x80) :
        pMLME->Work.Measure.Channel = 0;
        pMLME->Work.Measure.bkCCAMode = BBP_Read(0x13 );
        pMLME->Work.Measure.bkEdTh = BBP_Read(0x35 );
        WSetCCA_ED(pMLME->pReq.MeasChannel->ccaMode, pMLME->pReq.MeasChannel->edThreshold);
        pWork->Mode = (3 + 1) ;
        pMLME->Work.Measure.sts = 0x00 ;
    case (0x01 | 0x80) :
        pMLME->Work.Measure.Counter = 0;
        pMLME->Work.Measure.CCA = 0;
        ch = WL_ReadByte(&pMLME->pReq.MeasChannel->channelList[pMLME->Work.Measure.Channel]);
        if ((ch == 0) || (pMLME->Work.Measure.Channel >= sizeof(pMLME->pReq.MeasChannel->channelList))) {
            pMLME->State = (0x04 | 0x80) ;
            break;
        }
        if (FLASH_VerifyCheckSum(0 ) != 0) {
            pMLME->Work.Measure.sts = 0x0E ;
            pMLME->State = (0x04 | 0x80) ;
            break;
        }
        if (pMLME->State == (0x00 | 0x80) ) {
            WSetChannel(ch, 0 );
            WStart();
            pMLME->Work.Measure.bkPowerMode = *(vu16 *)((0x04808000) + 0x040) ;
            WSetForcePowerState(((0x0000 << 0) | (0x0001 << 15)) );
        } else {
            WSetChannel(ch, 0 );
        }
        pMLME->State = (0x02 | 0x80) ;
        SetupTimeOut(pMLME->pReq.MeasChannel->measureTime, MLME_MeasChanTimeOut);
    case (0x02 | 0x80) :
        pMLME->Work.Measure.Counter++;
        if (*(vu16 *)((0x04808000) + 0x19C) & (0x0001 << 0) ) {
            pMLME->Work.Measure.CCA += 100;
        }
        break;
    case (0x03 | 0x80) :
        ch = WL_ReadByte(&pMLME->pReq.MeasChannel->channelList[pMLME->Work.Measure.Channel]);
        ratio = 0;
        if (pMLME->Work.Measure.Counter != 0) {
            if (pMLME->Work.Measure.CCA) {
                ratio = (pMLME->Work.Measure.CCA / pMLME->Work.Measure.Counter) + 1;
                if (ratio > 100) {
                    ratio = 100;
                }
            }
        }
        pMLME->pCfm.MeasChannel->ccaBusyInfo[pMLME->Work.Measure.Channel] = ch | (ratio << 8);
        pMLME->Work.Measure.Channel++;
        pMLME->State = (0x01 | 0x80) ;
        break;
    case (0x04 | 0x80) :
        WStop();
        pWork->Mode = ((LPWL_MAN)native_host_arm7_data_0380fff4) ->Config.Mode;
        BBP_Write(0x13 , pMLME->Work.Measure.bkCCAMode);
        BBP_Write(0x35 , pMLME->Work.Measure.bkEdTh);
        WSetForcePowerState(pMLME->Work.Measure.bkPowerMode);
        pMLME->pCfm.MeasChannel->resultCode = pMLME->Work.Measure.sts;
        pMLME->State = 0x00 ;
        {
            u32 remainingChannel;
            for (remainingChannel = pMLME->Work.Measure.Channel; remainingChannel < sizeof(pMLME->pReq.MeasChannel->channelList); remainingChannel++) {
                pMLME->pCfm.MeasChannel->ccaBusyInfo[remainingChannel] = 0;
            }
        }
        IssueMlmeConfirm();
        break;
    }
    if (pMLME->State != 0x00 ) {
        AddTask(2 , 5 );
    }
}
void MLME_MeasChanTimeOut(void *arg)
{
    ((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.State = (0x03 | 0x80) ;
    AddTask(2 , 5 );
}
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
