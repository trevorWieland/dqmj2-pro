typedef struct {
    MAC_HEADER MacHeader;
    DATA_HEADER Dot11Header;
    u8 Body[4];
} RXFRM_MAC, *LPRXFRM_MAC;

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

u32 native_utility_child_arm7_arm_027f52a8(LPRXFRM pFrm);

void native_utility_child_arm7_arm_027f50e4(LPRXFRM pFrm);

u32 native_utility_child_arm7_arm_027f5000(LPRXFRM pFrm);

void native_utility_child_arm7_arm_027f4940(LPBEACON_FRAME pFrm);

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

void *native_utility_child_arm7_arm_037fa9a0(void *p);

void native_utility_child_arm7_wram_037fac70(void);

static LPRXFRM native_utility_child_arm7_arm_037fb1f8(LPRXFRM_MAC pMFrm, u32 length)
    __attribute__((never_inline));
