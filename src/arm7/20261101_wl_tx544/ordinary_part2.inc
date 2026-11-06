typedef struct {
	u16			state;
	u16			aid;
	u16			macAdrs[3];
	u16			rssi;
	u16			capaInfo;
	u16			authSeed;
	u16			supRateSet;
	u16			rsv;
	u16			lastSeqCtrl;
	u16			frameCount;
	u16			lifeTime;
	u16			maxLifeTime;
} WlStaElement;

typedef	struct {
	u16	rssi;
	u16	channel;
	u16	capaInfo;
	u16	bssid[3];
	u16	ssidLength;
	u8	ssid[32];
	u16	beaconInterval;
	u16	lifeTime;
} WlApElement;

extern const u16 (*ctrdgi_fl_maxtime);

typedef struct {
    u16 NextId;
    u16 Flag;
    void (*pTaskFunc)(void);
} TASK_TBL, *LPTASK_TBL;

typedef struct {
    u16 EnQ[4 ];
    u16 DeQ[4 ];
    vu16 NextPri;
    u16 TaskPri;
    u16 CurrTaskID;
    u16 pad;
    OSThread Thread;
    TASK_TBL TaskTbl[24 ];
} TASK_MAN, *LPTASK_MAN;

typedef struct {
    u32 Prev;
    u32 Next;
    u16 Flag;
    u16 BufID;
} HEAPBUF_HEADER, *LPHEAPBUF_HEADER;

typedef struct {
    LPHEAPBUF_HEADER Head;
    LPHEAPBUF_HEADER Tail;
    u16 Count;
    u16 Flag;
} HEAPBUF_MAN, *LPHEAPBUF_MAN;

typedef struct {
    u32 heapType;
    union {
        struct {
            OSArenaId id;
            OSHeapHandle heapHandle;
        } os;
        struct {
            u32 (*alloc)(u32 size);
            u32 (*free)(void *p);
        } ext;
    } func;
} HEAP_INFO, *LPHEAP_INFO;

typedef struct {
    HEAP_INFO HeapInfo;
    HEAPBUF_MAN TmpBuf;
    HEAPBUF_MAN TxPri[3];
    HEAPBUF_MAN MaDataCfm;
    HEAPBUF_MAN RxData;
    HEAPBUF_MAN RxBeacon;
    HEAPBUF_MAN RxManCtrl;
    HEAPBUF_MAN Defrag;
    HEAPBUF_MAN ToWM;
    HEAPBUF_MAN RequestCmd;
    HEAPBUF_MAN man_rsv[4];
} HEAP_MAN, *LPHEAP_MAN;

void *AllocateHeapBuf(LPHEAPBUF_MAN pBufMan, u32 Length);

u32 ReleaseHeapBuf(LPHEAPBUF_MAN pBufMan, void *pBuf);

void *GetHeapBufNextAdrs(void *pBuf);

typedef struct {
    u16 FrameId;
    u16 CamAdrs;
    u16 FrameTime;
    u16 Length;
} FIRM_HEADER, *LPFIRM_HEADER;

typedef union {
    struct {
        u16 Status;
        u16 Status2;
        u16 rsv_RetryCount;
        u16 rsv_AppRate;
        u16 Service_Rate;
        u16 MPDU;
    } Tx;
    struct {
        u16 Status;
        u16 NextBnry;
        u16 TimeStamp;
        u16 Service_Rate;
        u16 MPDU;
        u16 rsv_RSSI;
    } Rx;
} MAC_HEADER, *LPMAC_HEADER;

typedef union {
    u16 Data;
    struct {
        u16 Version : 2;
        u16 Type : 2;
        u16 SubType : 4;
        u16 ToDS : 1;
        u16 FromDS : 1;
        u16 MoreFrag : 1;
        u16 Retry : 1;
        u16 PowerMan : 1;
        u16 MoreData : 1;
        u16 WEP : 1;
        u16 Order : 1;
    } Bit;
} FRAME_CTRL, *LPFRAME_CTRL;

typedef union {
    u16 Data;
    struct {
        u16 FragNum : 4;
        u16 SeqNum : 12;
    } Bit;
} SEQ_CTRL, *LPSEQ_CTRL;

typedef struct {
    FRAME_CTRL FrameCtrl;
    u16 Duration;
    u16 DA[3];
    u16 SA[3];
    u16 BSSID[3];
    SEQ_CTRL SeqCtrl;
} MAN_HEADER, *LPMAN_HEADER;

typedef struct {
    u16 ReasonCode;
} DISASS_BODY, *LPDISASS_BODY;

typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    DISASS_BODY Body;
} DISASS_FRAME, *LPDISASS_FRAME;

typedef struct {
    FRAME_CTRL FrameCtrl;
    u16 DurationID;
    u16 Adrs1[3];
    u16 Adrs2[3];
    u16 Adrs3[3];
    SEQ_CTRL SeqCtrl;
} DATA_HEADER, *LPDATA_HEADER;

typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    DATA_HEADER Dot11Header;
    union {
        u8 Body[4];
        u8 *Pointer;
    } Data;
} TXFRM, *LPTXFRM;

typedef struct {
    MAC_HEADER MacHeader;
    DATA_HEADER Dot11Header;
    u8 Body[4];
} TXFRM_MAC, *LPTXFRM_MAC;

typedef struct {
    u16 Busy;
    u16 InCount;
    u16 OutCount;
    u16 pad;
    LPTXFRM_MAC pMacFrm;
    LPTXFRM pFrm;
    void (*pEndFunc)(LPTXFRM pFrm, u32 flag);
} TXQ, *LPTXQ;

typedef struct {
    TXQ Txq[3];
    TXQ Mp;
    TXQ Key[2];
    TXQ Beacon;
    u32 Flag;
    WlMaMpEndInd *pMpEndInd;
    u16 TXOP;
    u16 TMPTT;
    u16 SetKeyMap;
    u16 GetKeyMap;
    u16 DataLength;
    u16 RetryLimit;
    u16 RestBitmap;
    u16 BkKeyIn;
    u16 BkKeyOut;
    u16 BkSeqNum;
    u16 MpBlkCnt;
    u16 MpRstCnt;
    u16 MpLastOk;
    u16 TimeOutFrm;
} TX_CTRL, *LPTX_CTRL;

void TxqPri(u32 pri);

void CopyTxFrmToMacBuf(LPTXFRM_MAC pMacTxFrm, WlMaDataReq *pTxReq);

u32 CheckFrameTimeout(LPTXFRM pTxFrm);

void DeleteAllTxFrames(void);

void MessageDeleteTx(u32 pri, u32 bMsg);

void ClearTxKeyData(void);

void ClearQueuedPri(u32 pri);

void StartBeaconFrame(void);

void StopBeaconFrame(void);

void TxPsPollFrame(void);

LPDISASS_FRAME MakeDisAssFrame(u16 *pDA, u16 reasonCode);

void MakePsPollFrame(u16 aid);

u32 IsExistManFrame(u16 *pDA, u16 frameCtrl);

void InitManHeader(LPTXFRM pFrm, u16 *pDA);

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

u32 CAM_GetStaState(u32 camAdrs);

u32 CAM_IsActive(u32 camAdrs);

u32 CAM_GetFrameCount(u32 camAdrs);

void CAM_DecFrameCount(LPTXFRM pFrm);

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

u16 WSetPowerState(u32 state);

void WClearKSID(void *arg);

void WSetMacAdrs2(u16 *dst, u16 *src1, u16 *src2);

void WSetMacAdrs3(u16 *dst, u16 *src1, u16 *src2, u16 *src3);

void WUpdateCounter(void);

u32 MatchMacAdrs(u16 *pAdrs1, u16 *pAdrs2);

u32 WCalcManRate(void);

void DMA_Write(void *destAdrs, void *srcAdrs, u32 length);

void DMA_WriteHeaderData(LPTXFRM_MAC destAdrs, LPMAC_HEADER header, u8 *data, u32 length);

void DMA_WepWriteHeaderData(LPTXFRM_MAC destAdrs, LPMAC_HEADER header, u8 *data, u32 length);

void SetFatalErr(u32 errCode);
