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

u32 RxMpAckFrame(LPRXFRM pFrm);

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

void RxDisAssFrame(LPDISASS_FRAME pFrm);

void RxDeAuthFrame(LPDEAUTH_FRAME pFrm);

void ElementChecker(LPELEMENT_CHECKER p);

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

u32 RxMpAckFrame(LPRXFRM pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    WlMaMpAckInd *pInd;
    if (((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work.STA != 0x40 ) {
        return 1;
    }
    if ((MatchMacAdrs(pFrm->Dot11Header.Adrs2, pWork->BSSID) == 0) || (MatchMacAdrs(pFrm->Dot11Header.Adrs3, pWork->LinkAdrs) == 0)) {
        ;
        return 1;
    }
    ;
    pFrm->FirmHeader.Length = pFrm->MacHeader.Rx.MPDU - 24 - 2 - 2;
    pInd = (WlMaMpAckInd *)(void *)((u32)pFrm - (sizeof(WlMaDataReq) - sizeof(WlTxFrame))) ;
    pInd->header.code = (0x0100 | 0x85) ;
    pInd->header.length = ((sizeof(WlRxMpAckFrame)+1)/2) ;
    pInd->ack.txKeySts |= (((LPWL_MAN)native_host_arm7_data_0380fff4) ->RxCtrl.TxKeyReg | ((*(vu16 *)((0x04808000) + 0x098) & 0x8000) >> 4) | ((*(vu16 *)((0x04808000) + 0x094) & 0x8000) >> 3));
    SendMessageToWmDirect(&((LPWL_MAN)native_host_arm7_data_0380fff4) ->HeapMan.TmpBuf, pInd);
    ;
    return 0;
}

void RxDisAssFrame(LPDISASS_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPDEAUTH_FRAME pDeAuth;
    u32 st, cam_adrs;
    ;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    switch (pWork->Mode) {
    case 1 :
        st = CAM_GetStaState(cam_adrs);
        if (st == 0x40 ) {
            CAM_SetStaState(cam_adrs, 0x30 );
            MLME_IssueDisAssIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
            DeleteTxFrames(cam_adrs);
        } else {
            if (st == 0x30 ) {
                pDeAuth = (LPDEAUTH_FRAME)MakeDisAssFrame(pFrm->Dot11Header.SA, 7 );
            } else {
                pDeAuth = MakeDeAuthFrame(pFrm->Dot11Header.SA, 7 , 1 );
            }
            if ((u32)pDeAuth != (0) ) {
                TxManCtrlFrame((LPTXFRM)pDeAuth);
            }
        }
        break;
    case 2 :
    case 3 :
        if ((pWork->STA == 0x40 ) && (MatchMacAdrs(pFrm->Dot11Header.SA, pWork->LinkAdrs))) {
            WSetStaState(0x30 );
            WClearAids();
            MLME_IssueDisAssIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
        }
        break;
    }
}

void RxDeAuthFrame(LPDEAUTH_FRAME pFrm)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    LPDEAUTH_BODY pDeAuth;
    u32 bodyLen, cam_adrs;
    bodyLen = pFrm->FirmHeader.Length;
    pDeAuth = &pFrm->Body;
    ;
    cam_adrs = pFrm->FirmHeader.CamAdrs;
    switch (pWork->Mode) {
    case 1 :
        if (CAM_GetStaState(cam_adrs) > 0x20 ) {
            CAM_SetStaState(cam_adrs, 0x20 );
            MLME_IssueDeAuthIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
            DeleteTxFrames(cam_adrs);
        }
        break;
    case 2 :
    case 3 :
        if ((pWork->STA > 0x20 ) && (MatchMacAdrs(pFrm->Dot11Header.SA, pWork->LinkAdrs))) {
            WSetStaState(0x20 );
            WClearAids();
            MLME_IssueDeAuthIndication(pFrm->Dot11Header.SA, pFrm->Body.ReasonCode);
            break;
        }
    }
}

void ElementChecker(LPELEMENT_CHECKER p)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)native_host_arm7_data_0380fff4) ->Work;
    u8 *pBuf;
    s32 i;
    u32 id, len;
    pBuf = p->pElement;
    p->channel = pWork->CurrChannel;
    if (p->foundFlag & 0x0800 ) {
        p->matchFlag |= 0x0001 ;
    }
    for (i = p->bodyLength; i > 0;) {
        id = WL_ReadByte(pBuf++);
        len = WL_ReadByte(pBuf++);
        switch (id) {
        case 0 :
            if (len <= 32 ) {
                p->foundFlag |= 0x0001 ;
                p->pSSID = (LPSSID_ELEMENT)&pBuf[-2];
                if ((len == 0) && (p->foundFlag & 0x0800 )) {
                    p->matchFlag |= 0x0001 ;
                } else {
                    p->matchFlag &= ~0x0001 ;
                    if (WCheckSSID(len, pBuf)) {
                        p->matchFlag |= 0x0001 ;
                    }
                }
            }
            break;
        case 1 :
            if (len < 1) {
                break;
            }
            p->foundFlag |= 0x0004 ;
            WElement2RateSet((LPSUP_RATE_ELEMENT)&pBuf[-2], &p->rateSet);
            if (((p->rateSet.Basic & ~(pWork->RateSet.Basic | pWork->RateSet.Support)) == 0) && (((p->rateSet.Basic | p->rateSet.Support) & pWork->RateSet.Basic) == pWork->RateSet.Basic)) {
                p->matchFlag |= 0x0004 ;
            } else {
                p->matchFlag &= ~0x0004 ;
            }
            break;
        case 2 :
            break;
        case 3 :
            if (len < 1) {
                break;
            }
            p->foundFlag |= 0x0002 ;
            p->channel = WL_ReadByte(&pBuf[0]);
            if (p->channel == ((LPWL_MAN)native_host_arm7_data_0380fff4) ->MLME.pReq.Join->bssDesc.channel) {
                p->matchFlag |= 0x0002 ;
            } else {
                p->matchFlag &= ~0x0002 ;
            }
            break;
        case 5 :
            if (len < 3) {
                break;
            }
            p->foundFlag |= 0x0100 ;
            p->pTIM = (LPTIM_ELEMENT)&pBuf[-2];
            break;
        case 4 :
            if (len < 6) {
                break;
            }
            p->foundFlag |= 0x0200 ;
            p->pCFP = (LPCF_PARAM_ELEMENT)&pBuf[-2];
            break;
        case 6 :
            break;
        case 221 :
            if ((len < 3 + 1 + 4) || (WL_ReadByte(&pBuf[0]) != 0x00 ) || (WL_ReadByte(&pBuf[1]) != 0x09 ) || (WL_ReadByte(&pBuf[2]) != 0xBF ) || (WL_ReadByte(&pBuf[3]) != 0x00 )) {
                p->otherElementCount++;
                p->otherElementLength += (len + 2);
            } else {
                p->foundFlag |= 0x0400 ;
                p->pGMIF = (LPGAME_INFO_ELEMENT)&pBuf[-2];
            }
            break;
        default:
            p->otherElementCount++;
            p->otherElementLength += (len + 2);
        }
        pBuf += len;
        i -= (len + 2);
    }
    if (p->foundFlag & 0x0008 ) {
        if ((pWork->BSSID[0] & 0x0001) || (p->rxStatus & (0x0001 << 15) )) {
            p->matchFlag |= 0x0008 ;
        }
    }
    if (p->foundFlag & 0x0030 ) {
        if ((p->capability & ((0x01 << 0) | (0x01 << 1) )) == (pWork->CapaInfo & ((0x01 << 0) | (0x01 << 1) ))) {
            p->matchFlag |= 0x0010 ;
        }
        if ((p->capability & (0x01 << 4) ) == (pWork->CapaInfo & (0x01 << 4) )) {
            p->matchFlag |= 0x0020 ;
        }
    }
}
