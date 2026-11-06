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

u32 native_host_arm7_arm_037f8908(LPHEAPBUF_MAN pBufMan, void *pBuf);

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

typedef union {
    u16 Data;
    struct {
        u16 ESS : 1;
        u16 IBSS : 1;
        u16 CFPollable : 1;
        u16 CFPollRequest : 1;
        u16 Privacy : 1;
        u16 ShortPreamble : 1;
        u16 rsv6 : 1;
        u16 rsv7 : 1;
        u16 rsv8 : 1;
        u16 rsv9 : 1;
        u16 rsv10 : 1;
        u16 rsv11 : 1;
        u16 rsv12 : 1;
        u16 rsv13 : 1;
        u16 rsv14 : 1;
        u16 rsv15 : 1;
    } Bit;
} CAPA_INFO, *LPCAPA_INFO;

typedef struct {
    u8 ID;
    u8 Length;
    u8 SSID[32];
} SSID_ELEMENT, *LPSSID_ELEMENT;

typedef struct {
    u8 ID;
    u8 Length;
    u8 SupportedRate[2];
} SUP_RATE_ELEMENT, *LPSUP_RATE_ELEMENT;

typedef struct {
    u8 ID;
    u8 Length;
    u8 Text[253];
} CHALLENGE_ELEMENT, *LPCHALLENGE_ELEMENT;

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
    CAPA_INFO CapaInfo;
    u16 StatusCode;
    u16 AID;
    u8 Buf[sizeof(SUP_RATE_ELEMENT)];
} ASSRES_BODY, *LPASSRES_BODY;

typedef struct {
    u16 AlgoType;
    u16 SeqNum;
    u16 StatusCode;
    CHALLENGE_ELEMENT ChallengeText;
    u8 pad[1];
} AUTH_BODY, *LPAUTH_BODY;

typedef struct {
    u16 ReasonCode;
} DEAUTH_BODY, *LPDEAUTH_BODY;

typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    DISASS_BODY Body;
} DISASS_FRAME, *LPDISASS_FRAME;

typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    ASSRES_BODY Body;
} ASSRES_FRAME, *LPASSRES_FRAME;

typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    AUTH_BODY Body;
} AUTH_FRAME, *LPAUTH_FRAME;

typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    DEAUTH_BODY Body;
} DEAUTH_FRAME, *LPDEAUTH_FRAME;

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

void native_host_arm7_arm_027eff00(u32 pri);

void native_host_arm7_main_027f0484(LPTXFRM pFrm, u32 flag);

void TxManCtrlFrame(LPTXFRM pFrm);

void native_host_arm7_arm_027f10a0(LPTXFRM pFrm);

LPDEAUTH_FRAME native_host_arm7_arm_027f1ec8(u16 *pDA, u16 reasonCode, u32 bCheck);

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

void native_host_arm7_arm_027ebc50(u16 camAdrs, u16 state);

void native_host_arm7_arm_027ebdb4(u32 camAdrs);

u32 native_host_arm7_arm_027ebfec(u32 camAdrs);

u32 native_host_arm7_arm_027ec02c(u32 camAdrs);

void native_host_arm7_arm_027ebbe0(LPTXFRM pFrm);

void native_host_arm7_arm_027ebf6c(u16 camAdrs);

void native_host_arm7_arm_027ec438(u16 camAdrs);

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

void native_host_arm7_arm_037f9238(u32 state);

void native_host_arm7_arm_027ea048(void);
