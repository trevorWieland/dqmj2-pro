typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef void (*Handler)(void);
typedef u32 (*Step)(void);
typedef struct { Handler start; Step step; Handler finish; } Callbacks;

extern void func_ov003_021d7a78(void);
extern u32 func_ov003_021d7afc(void);
extern void func_ov003_021d7c70(void);
extern void func_ov003_021dadc4(void);
extern u32 func_ov003_021dae50(void);
extern void func_ov003_021daf7c(void);
extern void func_ov003_021db9bc(void);
extern u32 func_ov003_021dba20(void);
extern void func_ov003_021dbae4(void);
extern void func_ov003_021dbca0(void);
extern u32 func_ov003_021dbd18(void);
extern void func_ov003_021dbdec(void);
extern void func_ov003_021dc214(void);
extern u32 func_ov003_021dc258(void);
extern void func_ov003_021dc500(void);
extern void func_ov003_021dcd3c(void);
extern u32 func_ov003_021dcd84(void);
extern void func_ov003_021dce34(void);
extern void func_ov003_021dd074(void);
extern u32 func_ov003_021dd0a4(void);
extern void func_ov003_021dd19c(void);
extern void func_ov003_021dd28c(void);
extern void func_ov003_021dd300(void);
extern void func_ov003_021dd5f4(void);
extern void func_ov003_021dd6c4(void);
extern void func_ov003_021dd8a4(void);
extern void func_ov003_021dd94c(void);
extern void func_ov003_021dda30(void);
extern void func_ov003_021ddad8(void);
extern void func_ov003_021ddbc0(void);
extern void func_ov003_021ddc68(void);
extern void func_ov003_021ddd4c(void);
extern void func_ov003_021dddf4(void);
extern void func_ov003_021dded8(void);
extern void func_ov003_021ddf80(void);
extern void func_ov003_021de09c(void);
extern u32 func_ov003_021de0f0(void);
extern void func_ov003_021de180(void);
extern void func_ov003_021de378(void);
extern u32 func_ov003_021de3d4(void);
extern void func_ov003_021de484(void);
extern u8 data_ov003_021e0e14[];
extern u8 data_ov003_021e0d3c[];

typedef struct {
    Callbacks initial[3];
    u16 catalogA[17];
    u16 catalogB[11];
    Callbacks modes[9];
    Handler panels[14];
    u16 bounds[4];
    u16 dimensions[2];
    void *work[2];
} ReadOnlyData;

u32 native_ov003_bss[704];

const ReadOnlyData native_ov003_rodata = {
    {{func_ov003_021d7a78, func_ov003_021d7afc, func_ov003_021d7c70}, {0, 0, 0}, {0, 0, 0}},
    {556, 557, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 1537, 2055, 1558},
    {556, 557, 302, 303, 304, 598, 599, 600, 601, 602, 570},
    {{func_ov003_021dadc4, func_ov003_021dae50, func_ov003_021daf7c}, {func_ov003_021db9bc, func_ov003_021dba20, func_ov003_021dbae4}, {func_ov003_021dcd3c, func_ov003_021dcd84, func_ov003_021dce34}, {func_ov003_021dbca0, func_ov003_021dbd18, func_ov003_021dbdec}, {func_ov003_021de09c, func_ov003_021de0f0, func_ov003_021de180}, {func_ov003_021de378, func_ov003_021de3d4, func_ov003_021de484}, {func_ov003_021dd074, func_ov003_021dd0a4, func_ov003_021dd19c}, {func_ov003_021dc214, func_ov003_021dc258, func_ov003_021dc500}, {0, 0, 0}},
    {func_ov003_021dd28c, func_ov003_021dd300, func_ov003_021dd5f4, func_ov003_021dd6c4, func_ov003_021dd8a4, func_ov003_021dd94c, func_ov003_021dda30, func_ov003_021ddad8, func_ov003_021ddbc0, func_ov003_021ddc68, func_ov003_021ddd4c, func_ov003_021dddf4, func_ov003_021dded8, func_ov003_021ddf80},
    {240, 64, 240, 152},
    {70, 54},
    {data_ov003_021e0e14, data_ov003_021e0d3c}
};

typedef struct {
    char text0[12];
    char text1[12];
    char text2[16];
    char text3[16];
    char text4[16];
    char text5[16];
    char text6[24];
    char text7[20];
    char text8[16];
    char text9[16];
    char text10[24];
    u16 firstCatalog[20];
    char systemA[20];
    char menu[20];
    char systemB[20];
    u16 secondCatalog[62];
    u8 rowsA[9][3];
    u8 rowsB[21][3];
    u8 reserved[2];
    u16 thirdCatalog[2];
    u8 flagsA[4];
    u8 flagsB[4];
    char objectBank[28];
} Data;

Data native_ov003_data = {
    "msg_virtual",
    "you_win.d16",
    "you_draw.d16",
    "you_lose.d16",
    "vs_start_1.d16",
    "vs_start_2.d16",
    "fld_up_menu_parts.cch",
    "MonsterIconDat.NICA",
    "ic_%04x.NCLD",
    "ic_%04x.NCGR",
    "fld_up_menu_parts.cch",
    {58, 0, 51, 52, 58, 59, 60, 51, 53, 54, 48, 49, 50, 55, 56, 57, 58, 0, 58, 0},
    "d2_SystemData.bin",
    "menu_parts_bg.cch",
    "d2_SystemData.bin",
    {1, 2, 3, 4, 5, 0, 12, 13, 16, 17, 34, 35, 51, 52, 58, 59, 60, 31, 32, 33, 44, 36, 37, 48, 49, 50, 38, 39, 40, 55, 56, 57, 41, 42, 43, 51, 53, 54, 18, 19, 20, 21, 42, 43, 44, 45, 24, 25, 26, 27, 28, 29, 33, 34, 35, 36, 37, 39, 23, 24, 16, 17},
    {{13, 1, 0}, {12, 1, 0}, {7, 1, 0}, {8, 1, 0}, {9, 1, 0}, {10, 1, 0}, {11, 1, 0}, {3, 1, 0}, {4, 1, 0}},
    {{12, 1, 3}, {0, 1, 1}, {1, 1, 1}, {2, 1, 1}, {3, 1, 1}, {4, 1, 1}, {5, 1, 1}, {6, 1, 1}, {7, 1, 1}, {8, 1, 1}, {9, 1, 1}, {10, 1, 1}, {11, 1, 1}, {13, 1, 1}, {14, 1, 1}, {15, 1, 1}, {16, 1, 1}, {17, 1, 1}, {127, 1, 1}, {127, 1, 1}, {127, 1, 1}},
    {0, 0},
    {58, 0},
    {1, 1, 0, 0},
    {1, 1, 0, 0},
    "d2_ObjKeepData.bin"
};
