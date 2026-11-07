void native_host_arm7_arm_027ebe38(u32 camAdrs, u32 SupRate);

void native_host_arm7_arm_027ebe58(u32 camAdrs, u32 seqCtrl);

void native_host_arm7_arm_027ebe98(u32 camAdrs);

u32 native_host_arm7_arm_027ebfec(u32 camAdrs);

u32 native_host_arm7_arm_027ec08c(u32 camAdrs);

u32 native_host_arm7_arm_027ec0d8(u32 camAdrs);

inline u32 LoadLow(u16 *p)
{
    return *p & 0x00FF;
}

typedef struct {
    u16 Basic;
    u16 Support;
} RATE_SET, *LPRATE_SET;

typedef struct {
    LPCAM_ELEMENT pCAM;
    u16 CamMaxStaNum;
    u16 MaxStaNum;
    u16 MacAdrs[3];
    u16 RetryLimit;
    u16 EnableChannel;
    u16 Mode;
    u16 Rate;
    u16 AuthAlgo;
    u16 WepMode;
    u16 WepKeyId;
    u16 FrameLifeTimePerBeacon;
    u16 BeaconType : 1;
    u16 BcSsidResponse : 1;
    u16 PreambleType : 1;
    u16 MainAntenna : 1;
    u16 Diversity : 1;
    u16 UseAntenna : 1;
    u16 BcnTxRxIndMsg : 1;
    u16 NullKeyRes : 1;
    u16 dmm : 8;
    u16 ActiveZone;
    u16 DiagResult;
    u32 ParamFlag;
} CONFIG_PARAM, *LPCONFIG_PARAM;

typedef struct {
    u64 NextTbttTsf;
    u16 STA;
    u16 RSSI;
    u16 Mode;
    u16 PowerMgtMode;
    u16 PowerState;
    u16 bSynchro;
    u16 RxDtims;
    u16 PN15Rate;
    u16 SigTest2;
    u16 bFirstTbtt;
    u16 ManCtrlRetry;
    u16 SSIDLength;
    u8 SSID[32 ];
    u8 SSIDMask[32 ];
    RATE_SET RateSet;
    u16 BSSID[3];
    u16 AID;
    u16 SeqNum;
    u16 BeaconPeriod;
    u16 ListenInterval;
    u16 CurrListenInterval;
    u16 DTIMPeriod;
    u16 DTIMCount;
    u16 rsvcc;
    u16 CurrChannel;
    u16 CapaInfo;
    u16 BeaconLostTh;
    u16 BeaconLostCnt;
    u16 LinkAdrs[3];
    u16 APCamAdrs;
    u16 FrameCtrl;
    u16 FrameLifeTime;
    u16 bExistTIM;
    u16 TxPower;
    struct {
        struct {
            u16 SSID;
            u16 TIM;
            u16 GameInfo;
        } Beacon;
        struct {
            u16 SSID;
        } ProbeReq;
        struct {
            u16 Size;
        } RxBuf;
    } Ofst;
    void *GameInfoAdrs;
    u16 GameInfoLength;
    u16 GameInfoAlign;
    u16 bUpdateGameInfo;
    u16 TmpttPs;
    u32 IntervalCount;
    u16 Scrambler;
    u16 DbgSeqNum;
    u16 FatalErr;
    u16 rsv;
    u16 CurrErrCount;
    u16 TxBufErrCount;
    u16 TxBufResCount;
    u16 WepErrCount;
    u16 MpEndErrCount;
    u16 NotPollTxErrCount;
} WORK_PARAM, *LPWORK_PARAM;

typedef struct {
    u16 a;
    u16 b;
    u16 seed;
    u16 rsv;
} RAND_CTRL, *LPRAND_CTRL;

typedef struct {
    u16 Id;
    u16 Bits;
    u16 InitNum;
    u16 ChanNum;
    u16 BbpCnt;
    u16 pad;
    u32 BkReg;
} RF_CONFIG, *LPRF_CONFIG;

void native_host_arm7_arm_027eabec(void);

void native_host_arm7_arm_037f9238(u32 state);

void native_host_arm7_arm_027ea00c(u16 aid);

void native_host_arm7_arm_027ea0ec(u16 *dst, u16 *src1);

u32 native_host_arm7_arm_027ea480(u16 *pAdrs1, u16 *pAdrs2);

typedef struct {
    u16 State;
    u16 pad;
    union {
        struct {
            u16 MaxConfirmLength;
            u16 ChannelCount;
            u16 bFound;
            u16 ElapseTime;
            u16 TxPeriod;
        } Scan;
        struct {
            u16 Result;
            u16 Status;
        } Join;
        struct {
            LPTXFRM pTxFrm;
        } DeAuth;
        struct {
            LPTXFRM pTxFrm;
        } DisAss;
        struct {
            u32 Counter;
            u32 CCA;
            u16 bkPowerMode;
            u16 bkCCAMode;
            u16 bkEdTh;
            u16 bkMode;
            u16 Channel;
            u16 sts;
        } Measure;
    } Work;
    union {
        WlMlmeResetReq *Reset;
        WlMlmePowerMgtReq *PwrMgt;
        WlMlmeScanReq *Scan;
        WlMlmeJoinReq *Join;
        WlMlmeAuthReq *Auth;
        WlMlmeDeAuthReq *DeAuth;
        WlMlmeAssReq *Ass;
        WlMlmeReAssReq *ReAss;
        WlMlmeDisAssReq *DisAss;
        WlMlmeStartReq *Start;
        WlMlmeMeasChanReq *MeasChannel;
    } pReq;
    union {
        WlCmdCfm *Cfm;
        WlMlmeResetCfm *Reset;
        WlMlmePowerMgtCfm *PwrMgt;
        WlMlmeScanCfm *Scan;
        WlMlmeJoinCfm *Join;
        WlMlmeAuthCfm *Auth;
        WlMlmeDeAuthCfm *DeAuth;
        WlMlmeAssCfm *Ass;
        WlMlmeReAssCfm *ReAss;
        WlMlmeDisAssCfm *DisAss;
        WlMlmeStartCfm *Start;
        WlMlmeMeasChanCfm *MeasChannel;
    } pCfm;
} MLME_MAN, *LPMLME_MAN;

u32 native_host_arm7_arm_027ede50(u16 *pMacAdrs, u16 reason);

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

void native_host_arm7_arm_027f284c(LPBEACON_FRAME pFrm);

void native_host_arm7_main_027f3f40(void);

typedef struct {
    u8 *pElement;
    u16 rxStatus;
    u16 capability;
    u16 bodyLength;
    u16 matchFlag;
    u16 foundFlag;
    u16 activeZone;
    u16 vtsf;
    u16 channel;
    RATE_SET rateSet;
    u16 otherElementCount;
    u16 otherElementLength;
    LPSSID_ELEMENT pSSID;
    LPCF_PARAM_ELEMENT pCFP;
    LPTIM_ELEMENT pTIM;
    LPGAME_INFO_ELEMENT pGMIF;
} ELEMENT_CHECKER, *LPELEMENT_CHECKER;

extern void native_host_arm7_arm_027f2e98(LPDISASS_FRAME pFrm);

extern void native_host_arm7_arm_027f2f78(LPASSREQ_FRAME pFrm);

static void RxAssResFrame(LPASSRES_FRAME pFrm);

static void RxReAssReqFrame(LPREASSREQ_FRAME pFrm);

static void RxReAssResFrame(LPREASSRES_FRAME pFrm);

extern void native_host_arm7_arm_027f3148(LPPRBREQ_FRAME pFrm);

extern void native_host_arm7_arm_027f31fc(LPPRBRES_FRAME pFrm, LPELEMENT_CHECKER pChk);

extern void native_host_arm7_arm_027f35cc(LPAUTH_FRAME pFrm);

extern void native_host_arm7_arm_027f3b6c(LPDEAUTH_FRAME pFrm);

static void RxPsPollFrame(LPPSPOLL_FRAME pFrm);

static void RxCfEndFrame(LPCFEND_FRAME pFrm);

extern void native_host_arm7_arm_027f3c1c(LPELEMENT_CHECKER p);

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

void native_host_arm7_arm_027f284c(LPBEACON_FRAME pFrm);

void native_host_arm7_arm_027f2e98(LPDISASS_FRAME pFrm);

void native_host_arm7_arm_027f2f78(LPASSREQ_FRAME pFrm);

static void RxAssResFrame(LPASSRES_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPMLME_MAN pMLME = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->MLME;
    LPASSRES_BODY pAssRes;
    u32 bodyLen;
    bodyLen = pFrm->FirmHeader.Length;
    pAssRes = &pFrm->Body;
    ;
    if ((pWork->Mode != 2 ) && (pWork->Mode != 3 )) {
        ;
        return;
    }
    if (pMLME->State == (0x01 | 0x50) ) {
        if (native_host_arm7_arm_027ea480(pMLME->pReq.Ass->peerMacAdrs, pFrm->Dot11Header.SA)) {
            native_host_arm7_arm_027eabec();
            if (pAssRes->StatusCode == 0 ) {
                native_host_arm7_arm_027ea00c(pAssRes->AID & 0x0FFF);
                native_host_arm7_arm_027f1f5c(pWork->AID);
                native_host_arm7_arm_027ea0ec(pWork->LinkAdrs, pFrm->Dot11Header.SA);
                pWork->APCamAdrs = native_host_arm7_arm_027eb90c(pFrm->Dot11Header.SA);
                native_host_arm7_arm_027ebc50(pWork->APCamAdrs, 0x40 );
            }
            if (pAssRes->StatusCode == 0x00 ) {
                pMLME->pCfm.Ass->resultCode = 0x00 ;
                pMLME->pCfm.Ass->statusCode = 0x00 ;
                native_host_arm7_arm_037f9238(0x40 );
            } else {
                pMLME->pCfm.Ass->resultCode = 0x0C ;
                pMLME->pCfm.Ass->statusCode = pAssRes->StatusCode;
            }
            pMLME->pCfm.Ass->aid = pWork->AID;
            pMLME->State = (0x03 | 0x50) ;
            native_host_arm7_arm_037f8598(2 , 3 );
        }
    }
}

static void RxReAssReqFrame(LPREASSREQ_FRAME pFrm)
{
    LPWL_MAN pWlMan = (LPWL_MAN)&((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->TaskMan;
    LPREASSREQ_BODY pReAssReq;
    LPDEAUTH_FRAME pTxDeAuthFrm;
    LPREASSRES_FRAME pTxFrm;
    u32 bodyLen;
    u16 stsCode, aid, cam_adrs;
    ELEMENT_CHECKER elementCheck;
    bodyLen = pFrm->FirmHeader.Length;
    pReAssReq = &pFrm->Body;
    aid = 0;
    if (bodyLen <= 2 + 2 + 6) {
        return;
    }
    ;
    if (pWlMan->Work.Mode != 1 ) {
        ;
        return;
    }
    if (native_host_arm7_arm_027f2000(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x03 * 0x0010)) )) {
        return;
    }
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    do {
        if (native_host_arm7_arm_027ebfec(cam_adrs) < 0x30 ) {
            if (native_host_arm7_arm_027f2000(pFrm->Dot11Header.SA, ((0x00 * 0x0004) | (0x0C * 0x0010)) )) {
                return;
            }
            pTxDeAuthFrm = native_host_arm7_arm_027f1ec8(pFrm->Dot11Header.SA, 6 , 1 );
            if ((u32)pTxDeAuthFrm != (0) ) {
                native_host_arm7_arm_027f1088((LPTXFRM)pTxDeAuthFrm);
            }
            return;
        }
        if (native_host_arm7_arm_027ebfec(cam_adrs) == 0x40 ) {
            native_host_arm7_arm_027ebc50(cam_adrs, 0x30 );
            native_host_arm7_arm_027ede50(pFrm->Dot11Header.SA, 1 );
        } else if (native_host_arm7_arm_027ec0d8(cam_adrs) != 0) {
            ;
            return;
        }
        MI_CpuClear32(&elementCheck, sizeof(elementCheck));
        elementCheck.pElement = pReAssReq->Buf;
        elementCheck.bodyLength = bodyLen - (2 + 2 + 6);
        elementCheck.foundFlag = 0x0800 ;
        native_host_arm7_arm_027f3c1c(&elementCheck);
        if ((pReAssReq->CapaInfo.Data & 0xFFC2 ) || ((pWlMan->Config.WepMode == 0 ) && (pReAssReq->CapaInfo.Bit.Privacy == 1)) || ((pWlMan->Config.WepMode != 0 ) && (pReAssReq->CapaInfo.Bit.Privacy == 0))) {
            stsCode = 10 ;
            break;
        }
        native_host_arm7_arm_027ebe18(cam_adrs, pReAssReq->CapaInfo.Data);
        if ((elementCheck.matchFlag & 0x0001 ) == 0) {
            stsCode = 1 ;
            break;
        }
        if ((elementCheck.matchFlag & 0x0004 ) == 0) {
            stsCode = 18 ;
            break;
        }
        native_host_arm7_arm_027ebe38(cam_adrs, elementCheck.rateSet.Support);
        stsCode = 0 ;
    } while (0 );
    pTxFrm = native_host_arm7_arm_027f19fc(cam_adrs, stsCode, elementCheck.pSSID);
    if ((u32)pTxFrm != (0) ) {
        native_host_arm7_arm_027f1088((LPTXFRM)pTxFrm);
    }
}
