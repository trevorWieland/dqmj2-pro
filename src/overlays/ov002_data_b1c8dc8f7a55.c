typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;

extern void func_ov002_021d8514(void);
extern void func_ov002_021d85c4(void);
extern void func_ov002_021d8724(void);
extern void func_ov002_021d89dc(void);
extern void func_ov002_021d89fc(void);
extern void func_ov002_021d8aa8(void);
extern void func_ov002_021d8b24(void);
extern void func_ov002_021d8ba8(void);
extern void func_ov002_021d8ccc(void);

u32 native_ov002_bss[888];

typedef struct {
    u16 field0[6];
    const void *pointers[6];
    u16 field36[4];
    u16 field44[4];
    u16 field52[2];
    u16 field56[19];
    u16 field94[2];
    u16 field98[25];
    void (*callbacks[9])(void);
    u32 reserved[3];
} ReadOnlyData;

const ReadOnlyData native_ov002_rodata = {
    {32, 16, 17, 240, 7, 240},
    {
        (u8 *)native_ov002_bss + 160,
        (u8 *)native_ov002_bss + 28,
        (u8 *)native_ov002_bss + 92,
        (u8 *)native_ov002_bss + 1248,
        (u8 *)native_ov002_bss,
        (u8 *)native_ov002_bss + 288
    },
    {240, 64, 240, 152},
    {1, 2, 3, 0},
    {23, 1},
    {48, 52, 24, 70, 15, 76, 122, 2, 91, 137, 33, 93, 139, 53, 126, 172, 14, 179, 225},
    {7, 0},
    {1, 7, 0, 8, 3, 0, 15, 3, 0, 18, 4, 0, 21, 6, 0, 25, 5, 0, 31, 4, 0, 36, 8, 0, 40},
    {
        func_ov002_021d8514, func_ov002_021d85c4, func_ov002_021d8724,
        func_ov002_021d89dc, func_ov002_021d89fc, func_ov002_021d8aa8,
        func_ov002_021d8b24, func_ov002_021d8ba8, func_ov002_021d8ccc
    },
    {0, 0, 0}
};

typedef struct {
    u8 firstFlags[4];
    u8 secondFlags[4];
    char resource0[24];
    u8 table9[9][3];
    u8 table21[21][3];
    u16 reserved;
    char resource1[12];
    char resource2[12];
    char resource3[12];
    char resource4[12];
    char resource5[20];
    char resource6[32];
} InitializedData;

InitializedData native_ov002_data = {
    {1, 1, 0, 0},
    {1, 1, 0, 0},
    "d2_ObjCommonData.bin",
    {{13, 1, 2}, {12, 1, 2}, {7, 1, 2}, {8, 1, 2}, {9, 1, 2}, {10, 1, 2}, {11, 1, 2}, {3, 1, 2}, {4, 1, 2}},
    {
        {12, 1, 3}, {0, 1, 3}, {1, 1, 3}, {3, 1, 3}, {2, 1, 3}, {13, 1, 3}, {14, 1, 3},
        {5, 1, 3}, {6, 1, 3}, {7, 1, 3}, {8, 1, 3}, {8, 1, 3}, {8, 1, 3}, {8, 1, 3},
        {8, 1, 3}, {8, 1, 3}, {8, 1, 3}, {8, 1, 3}, {8, 1, 3}, {8, 1, 3}, {8, 1, 3}
    },
    0,
    "flag.pal",
    "flag.bin",
    "msg_profile",
    "msg_wifi",
    "d2_SystemData.bin",
    "menu_parts_bg.cch"
};
