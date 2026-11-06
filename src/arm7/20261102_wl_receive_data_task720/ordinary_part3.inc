u32 IsExistManFrame(u16 *pDA, u16 frameCtrl);
typedef WlStaElement *LPCAM_ELEMENT;
typedef struct {
    u16 Count;
    u16 PowerMgtMode;
    u16 PowerState;
    u16 NotClass3;
    u16 NotSetTIM;
    u16 dmm;
    u16 ConnectSta;
    u16 UseAidMap;
} CAM_MAN, *LPCAM_MAN;
u32 CAM_Search(u16 *pMacAdrs);
u32 CAM_SearchAdd(u16 *pMacAdrs);
void CAM_SetStaState(u16 camAdrs, u16 state);
void CAM_SetRSSI(u16 camAdrs, u16 rssi);
void CAM_SetPowerMgtMode(u16 camAdrs, u16 pmtMode);
void CAM_SetAwake(u32 camAdrs);
void CAM_SetCapaInfo(u32 camAdrs, u32 capInfo);
void CAM_SetSupRate(u32 camAdrs, u32 SupRate);
void CAM_SetLastSeqCtrl(u32 camAdrs, u32 seqCtrl);
void CAM_SetAuthSeed(u32 camAdrs, u32 seed);
void CAM_UpdateLifeTime(u32 camAdrs);
u32 CAM_GetStaState(u32 camAdrs);
u32 CAM_GetAuthSeed(u32 camAdrs);
u32 CAM_GetLastSeqCtrl(u32 camAdrs);
u32 CAM_GetAID(u32 camAdrs);
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
void ClearTimeOut(void);
u16 WSetActiveZoneTime(u16 time, u32 update);
u16 WSetBeaconPeriod(u16 period);
u16 WSetDTIMPeriod(u16 period);
u16 WSetChannel(u16 channel, u32 bDirect);
u16 WSetPowerState(u32 state);
void WSetStaState(u32 state);
void WSetAids(u16 aid);
void WClearAids(void);
void WSetMacAdrs1(u16 *dst, u16 *src1);
u32 WCheckSSID(u16 len, u8 *pSSID);
u32 MatchMacAdrs(u16 *pAdrs1, u16 *pAdrs2);
void WElement2RateSet(LPSUP_RATE_ELEMENT pSup, LPRATE_SET pRateSet);
void WL_WriteByte(void *p, u8 data);
u8 WL_ReadByte(void *p);
void RND_seed(u32 seed);
u16 RND_rand(void);
extern const u16 NULL_ADRS[3];
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
u32 MLME_IssueDeAuthIndication(u16 *pMacAdrs, u16 reason);
u32 MLME_IssueDisAssIndication(u16 *pMacAdrs, u16 reason);
u32 MLME_IssueBeaconRecvIndication(void *pRxFrm);
void SendMessageToWmDirect(LPHEAPBUF_MAN pBufMan, void *pMsg);
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
void RxDataFrameTask(void);
void RxBeaconFrame(LPBEACON_FRAME pFrm);
void RxManCtrlTask(void);
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
static void RxDisAssFrame(LPDISASS_FRAME pFrm);
static void RxAssReqFrame(LPASSREQ_FRAME pFrm);
static void RxAssResFrame(LPASSRES_FRAME pFrm);
static void RxReAssReqFrame(LPREASSREQ_FRAME pFrm);
static void RxReAssResFrame(LPREASSRES_FRAME pFrm);
static void RxProbeReqFrame(LPPRBREQ_FRAME pFrm);
static void RxProbeResFrame(LPPRBRES_FRAME pFrm, LPELEMENT_CHECKER pChk);
static void RxAuthFrame(LPAUTH_FRAME pFrm);
static void RxDeAuthFrame(LPDEAUTH_FRAME pFrm);
static void RxPsPollFrame(LPPSPOLL_FRAME pFrm);
static void RxCfEndFrame(LPCFEND_FRAME pFrm);
static void ElementChecker(LPELEMENT_CHECKER p);
static void SetChallengeText(u32 camAdrs, LPAUTH_FRAME pFrm);
static u32 CheckChallengeText(LPAUTH_FRAME pFrm);
typedef WlApElement AP_LIST;
void UpdateApList(u16 channel, LPBEACON_FRAME pFrm, LPSSID_ELEMENT pSSID);
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
void RxDataFrameTask(void)
{
    LPDEAUTH_FRAME pDeAuth;
    WlMaDataInd *pInd;
    LPRXFRM pFrm;
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPHEAP_MAN pHeapMan = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan;
    WlCounter *pCounter = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Counter;
    u32 camAdrs, err;
    pInd = (WlMaDataInd *)((u32)(*(LPHEAPBUF_MAN)&pHeapMan->RxData).Head) ;
    if ((u32)pInd == (u32)(-1) ) {
        return;
    }
    if (pWork->STA != 0x40 ) {
        ReleaseHeapBuf(&pHeapMan->RxData, pInd);
        return;
    }
    pFrm = (LPRXFRM)&pInd->frame;
    if (pFrm->Dot11Header.FrameCtrl.Bit.ToDS) {
        if (pFrm->Dot11Header.Adrs3[0] & 0x0001) {
            pCounter->rx.multicast++;
        } else {
            pCounter->rx.unicast++;
        }
    } else {
        if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
            pCounter->rx.multicast++;
        } else {
            pCounter->rx.unicast++;
        }
    }
    pCounter->rx.fragment += (((pFrm->MacHeader.Rx.Status & (0x000F * (0x0001 << 4))) / (0x0001 << 4)) - 1);
    err = 1;
    switch (pWork->Mode) {
    case 1 :
        if (pFrm->Dot11Header.FrameCtrl.Data & (0x0100 | 0x0200 ) != 0x0100 ) {
            ;
            break;
        }
        camAdrs = CAM_Search(pFrm->Dot11Header.Adrs2);
        if ((camAdrs == 255 ) || (CAM_GetStaState(camAdrs) != 0x40 )) {
            if (CAM_GetStaState(camAdrs) == 0x30 ) {
                if (IsExistManFrame(pFrm->Dot11Header.Adrs2, ((0x00 * 0x0004) | (0x0A * 0x0010)) )) {
                    break;
                }
                pDeAuth = (LPDEAUTH_FRAME)MakeDisAssFrame(pFrm->Dot11Header.Adrs2, 7 );
            } else {
                if (IsExistManFrame(pFrm->Dot11Header.Adrs2, ((0x00 * 0x0004) | (0x0C * 0x0010)) )) {
                    break;
                }
                pDeAuth = MakeDeAuthFrame(pFrm->Dot11Header.Adrs2, 7 , 1 );
            }
            if ((u32)pDeAuth != (0) ) {
                TxManCtrlFrame((LPTXFRM)pDeAuth);
            }
            break;
        }
        CAM_SetPowerMgtMode(camAdrs, pFrm->Dot11Header.FrameCtrl.Bit.PowerMan);
        if (pFrm->Dot11Header.SeqCtrl.Data == CAM_GetLastSeqCtrl(camAdrs)) {
            pCounter->rx.duplicateErr++;
            break;
        }
        WSetMacAdrs1(pFrm->Dot11Header.Adrs1, pFrm->Dot11Header.Adrs3);
        err = 0;
        break;
    case 2 :
    case 3 :
        if (pFrm->Dot11Header.FrameCtrl.Data & (0x0100 | 0x0200 ) != 0x0100 ) {
            ;
            break;
        }
        if (pWork->PowerMgtMode != 0x00 ) {
            if ((pFrm->Dot11Header.FrameCtrl.Data & 0x2000 ) == 0) {
                if (pFrm->Dot11Header.Adrs1[0] & 0x0001) {
                    pWork->bExistTIM &= ~0x01 ;
                } else {
                    if (pWork->Mode != 3 ) {
