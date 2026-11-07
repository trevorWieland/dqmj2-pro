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

void native_host_arm7_arm_027f4e1c(u32 adrs, u32 size, u8 *pBuf);

extern const u16 native_host_arm7_data_027f730c[40] __attribute__((aligned(4)));

extern const u16 native_host_arm7_data_027f72ac[16] __attribute__((aligned(4)));

u16 native_host_arm7_arm_027e8e68(u16 *pMacAdrs);

u16 native_host_arm7_arm_027e8ec8(u16 retry);

u16 native_host_arm7_arm_027e8efc(u16 enableChannel);

u16 native_host_arm7_arm_027e8f3c(u16 mode);

u16 native_host_arm7_arm_027e8fbc(u16 rate);

u16 native_host_arm7_arm_027e8ff0(u16 mode);

u16 native_host_arm7_arm_027e9090(u16 keyId);

u16 native_host_arm7_arm_027e90b4(u16 *pKey);

u16 native_host_arm7_arm_027e9114(u16 type);

u16 native_host_arm7_arm_027e914c(u16 response);

u16 native_host_arm7_arm_027e9184(u16 threshold);

u16 native_host_arm7_arm_027e91bc(u16 time, u32 update);

u16 native_host_arm7_arm_027e926c(u16 *pMask);

u16 native_host_arm7_arm_027e929c(u16 type);

u16 native_host_arm7_arm_027e9344(u16 type);

u16 native_host_arm7_arm_027e9368(u32 ccaMode, u32 edThreshold);

u16 native_host_arm7_arm_027e93ac(u32 mainAntenna);

u16 native_host_arm7_arm_027e9414(u32 diversity, u32 useAntenna);

u16 native_host_arm7_arm_027e94e8(u32 mode);

u16 native_host_arm7_arm_027e9528(u32 mode);

u16 native_host_arm7_arm_027e96ec(u16 period);

extern const RATE_SET native_host_arm7_data_027f72a8;
