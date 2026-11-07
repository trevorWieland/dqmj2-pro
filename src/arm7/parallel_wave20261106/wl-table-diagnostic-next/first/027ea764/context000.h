typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef volatile u16 vu16;

extern const u16 (*ctrdgi_fl_maxtime);

void native_host_arm7_main_027ea764(void);

u32 native_host_arm7_arm_027ea5fc(u32 adrs, u32 data);

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

u32 native_host_arm7_arm_027ea5fc(u32 adrs, u32 data);
