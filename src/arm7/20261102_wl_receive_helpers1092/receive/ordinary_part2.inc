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
void AddTask(s32 nPriority, u32 nTaskID);
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
u32 ReleaseHeapBuf(LPHEAPBUF_MAN pBufMan, void *pBuf);
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
    u8 CurrChannel;
} DS_PARAM_ELEMENT, *LPDS_PARAM_ELEMENT;
typedef struct {
    u8 ID;
    u8 Length;
    u8 CFPCount;
    u8 CFPPeriod;
    union {
        u16 u16;
        u8 u8[2];
    } CFPMaxDuration;
    union {
        u16 u16;
        u8 u8[2];
    } CFPDurRemain;
} CF_PARAM_ELEMENT, *LPCF_PARAM_ELEMENT;
typedef struct {
    u8 ID;
    u8 Length;
    u8 DTIMCount;
    u8 DTIMPeriod;
    u8 BitmapCtrl;
    u8 VitrualBitmap[16 / 8 + 3];
} TIM_ELEMENT, *LPTIM_ELEMENT;
typedef struct {
    u8 ID;
    u8 Length;
    u8 Text[253];
} CHALLENGE_ELEMENT, *LPCHALLENGE_ELEMENT;
typedef struct {
    u8 ID;
    u8 Length;
    u8 OUI[3];
    u8 SubType;
    u8 ActZone[2];
    u8 VTSF[2];
    u8 GameInfo[3];
} GAME_INFO_ELEMENT, *LPGAME_INFO_ELEMENT;
typedef struct {
    FRAME_CTRL FrameCtrl;
    u16 Duration;
    u16 DA[3];
    u16 SA[3];
    u16 BSSID[3];
    SEQ_CTRL SeqCtrl;
} MAN_HEADER, *LPMAN_HEADER;
typedef struct {
    u32 TimeStamp[2];
    u16 BeaconInterval;
    CAPA_INFO CapaInfo;
    u8 Buf[sizeof(SSID_ELEMENT) + sizeof(SUP_RATE_ELEMENT) + sizeof(DS_PARAM_ELEMENT) + sizeof(GAME_INFO_ELEMENT) + 0];
    u8 pad[2];
} BEACON_BODY, *LPBEACON_BODY;
typedef struct {
    u16 ReasonCode;
} DISASS_BODY, *LPDISASS_BODY;
typedef struct {
    CAPA_INFO CapaInfo;
    u16 ListenInterval;
    u8 Buf[sizeof(SSID_ELEMENT) + sizeof(SUP_RATE_ELEMENT)];
} ASSREQ_BODY, *LPASSREQ_BODY;
typedef struct {
    CAPA_INFO CapaInfo;
    u16 StatusCode;
    u16 AID;
    u8 Buf[sizeof(SUP_RATE_ELEMENT)];
} ASSRES_BODY, *LPASSRES_BODY;
typedef struct {
    CAPA_INFO CapaInfo;
    u16 ListenInterval;
    u16 CurrAPMacAdrs[3];
    u8 Buf[sizeof(SSID_ELEMENT) + sizeof(SUP_RATE_ELEMENT)];
} REASSREQ_BODY, *LPREASSREQ_BODY;
typedef struct {
    CAPA_INFO CapaInfo;
    u16 StatusCode;
    u16 AID;
    u8 Buf[sizeof(SUP_RATE_ELEMENT)];
} REASSRES_BODY, *LPREASSRES_BODY;
typedef struct {
    u8 Buf[sizeof(SSID_ELEMENT) + sizeof(SUP_RATE_ELEMENT)];
} PRBREQ_BODY, *LPPRBREQ_BODY;
typedef struct {
    u32 TimeStamp[2];
    u16 BeaconInterval;
    CAPA_INFO CapaInfo;
    u8 Buf[sizeof(SSID_ELEMENT) + sizeof(SUP_RATE_ELEMENT) + sizeof(DS_PARAM_ELEMENT) + sizeof(GAME_INFO_ELEMENT)];
    u8 pad[2];
} PRBRES_BODY, *LPPRBRES_BODY;
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
    BEACON_BODY Body;
} BEACON_FRAME, *LPBEACON_FRAME;
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
    ASSREQ_BODY Body;
} ASSREQ_FRAME, *LPASSREQ_FRAME;
typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    REASSREQ_BODY Body;
} REASSREQ_FRAME, *LPREASSREQ_FRAME;
typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    REASSRES_BODY Body;
} REASSRES_FRAME, *LPREASSRES_FRAME;
typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    PRBRES_BODY Body;
} PRBRES_FRAME, *LPPRBRES_FRAME;
typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    MAN_HEADER Dot11Header;
    PRBREQ_BODY Body;
} PRBREQ_FRAME, *LPPRBREQ_FRAME;
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
    u16 BSSID[3];
    u16 TA[3];
} PSPOLL_HEADER, *LPPSPOLL_HEADER;
typedef struct {
    FIRM_HEADER FirmHeader;
    MAC_HEADER MacHeader;
    PSPOLL_HEADER Dot11Header;
} PSPOLL_FRAME, *LPPSPOLL_FRAME;
typedef struct {
    FRAME_CTRL FrameCtrl;
    u16 DurationID;
    u16 RA[3];
    u16 BSSID[3];
} CFEND_HEADER, *LPCFEND_HEADER;
typedef struct {
    CFEND_HEADER Header;
} CFEND_FRAME, *LPCFEND_FRAME;
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
void DeleteTxFrames(u32 camAdrs);
void TxManCtrlFrame(LPTXFRM pFrm);
void TxPsPollFrame(void);
LPDISASS_FRAME MakeDisAssFrame(u16 *pDA, u16 reasonCode);
LPASSRES_FRAME MakeAssResFrame(u16 camAdrs, u16 statusCode, LPSSID_ELEMENT pSSID);
LPREASSRES_FRAME MakeReAssResFrame(u16 camAdrs, u16 statusCode, LPSSID_ELEMENT pSSID);
LPPRBRES_FRAME MakeProbeResFrame(u16 *pDA);
LPAUTH_FRAME MakeAuthFrame(u16 *pDA, u16 txtLen, u32 bCheck);
