typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;

typedef struct { u8 indices[16]; s8 links[10][5]; u8 reserved[2]; } ReadOnlyData;
typedef struct { const char *first; const char *second; const char *third; } Resources;
typedef struct {
    u32 ordinal, first, second, kind;
    u16 field16, field18;
    s8 field20, field21;
    u16 reserved22;
    s32 coordinates[4];
    u8 field40, reserved41;
    u16 field42;
    u8 field44, reserved45[3];
} Row48;

u32 native_ov007_bss[600];

const ReadOnlyData native_ov007_rodata = {
    {2, 2, 0, 0, 13, 13, 2, 5, 7, 0, 0, 0, 0, 1, 2, 7},
    {
        {2, -1, 0, 0, 0},
        {1, -1, 0, 0, 0},
        {13, 3, -1, 0, 0},
        {6, -1, 0, 0, 0},
        {4, -1, 0, 0, 0},
        {5, -1, 0, 0, 0},
        {7, -1, 0, 0, 0},
        {7, 8, -1, 0, 0},
        {13, -1, 0, 0, 0},
        {7, 8, 15, -1, 0},
    },
    {0, 0}
};

typedef struct {
    char name_021da0c0[20];
    char name_021da0d4[8];
    char name_021da0dc[24];
    u32 selection[4];
    char name_021da104[28];
    char name_021da120[28];
    char name_021da13c[28];
    char name_021da158[28];
    char name_021da174[20];
    char name_021da188[20];
    char name_021da19c[20];
    char name_021da1b0[20];
    char name_021da1c4[20];
    char name_021da1d8[20];
    char name_021da1ec[20];
    char name_021da200[20];
    char name_021da214[20];
    char name_021da228[20];
    char name_021da23c[20];
    char name_021da250[20];
    char name_021da264[20];
    char name_021da278[20];
    char name_021da28c[20];
    char name_021da2a0[20];
    char name_021da2b4[20];
    char name_021da2c8[20];
    char name_021da2dc[20];
    char name_021da2f0[20];
    char name_021da304[20];
    char name_021da318[20];
    char name_021da32c[20];
    char name_021da340[20];
    char name_021da354[20];
    char name_021da368[20];
    char name_021da37c[20];
    char name_021da390[20];
    char name_021da3a4[20];
    char name_021da3b8[20];
    char name_021da3cc[24];
    char name_021da3e4[24];
    char name_021da3fc[24];
    char name_021da414[24];
    char name_021da42c[24];
    char name_021da444[24];
    char name_021da45c[24];
    char name_021da474[24];
    char name_021da48c[24];
    char name_021da4a4[24];
    char name_021da4bc[24];
    char name_021da4d4[24];
    char name_021da4ec[24];
    char name_021da504[24];
    char name_021da51c[24];
    Resources resources[15];
    Row48 rows[16];
    char name_021da8e8[20];
    char name_021da8fc[20];
    char name_021da910[12];
    char name_021da91c[8];
    s8 field924;
    u8 reserved925[3];
    char name_021da928[28];
    char name_021da944[28];
    char name_021da960[32];
} InitializedData;

InitializedData native_ov007_data = {
    "d2_SystemData.bin",
    "msg_map",
    "world_map_bg_%02d.wbg",
    {164, 104, 0, 0},
    "world_map_sub_bg_%02d.wbg",
    "world_map_sub_bg_%02d.chr",
    "world_map_sub_bg_%02d.scrn",
    "world_map_sub_bg_%02d.pal",
    "world_map_bg_11.pal",
    "world_map_bg_14.chr",
    "world_map_bg_03.chr",
    "world_map_bg_04.chr",
    "world_map_bg_05.pal",
    "world_map_bg_15.pal",
    "world_map_bg_09.pal",
    "world_map_bg_02.pal",
    "world_map_bg_13.pal",
    "world_map_bg_10.pal",
    "world_map_bg_04.pal",
    "world_map_bg_12.chr",
    "world_map_bg_05.chr",
    "world_map_bg_02.chr",
    "world_map_bg_11.chr",
    "world_map_bg_01.chr",
    "world_map_bg_01.pal",
    "world_map_bg_10.chr",
    "world_map_bg_15.chr",
    "world_map_bg_13.chr",
    "world_map_bg_09.chr",
    "world_map_bg_03.pal",
    "world_map_bg_08.pal",
    "world_map_bg_08.chr",
    "world_map_bg_12.pal",
    "world_map_bg_07.pal",
    "world_map_bg_07.chr",
    "world_map_bg_14.pal",
    "world_map_bg_06.pal",
    "world_map_bg_06.chr",
    "world_map_bg_06.scrn",
    "world_map_bg_11.scrn",
    "world_map_bg_07.scrn",
    "world_map_bg_08.scrn",
    "world_map_bg_12.scrn",
    "world_map_bg_14.scrn",
    "world_map_bg_15.scrn",
    "world_map_bg_01.scrn",
    "world_map_bg_02.scrn",
    "world_map_bg_09.scrn",
    "world_map_bg_03.scrn",
    "world_map_bg_04.scrn",
    "world_map_bg_10.scrn",
    "world_map_bg_13.scrn",
    "world_map_bg_05.scrn",
    {
        {native_ov007_data.name_021da2a0, native_ov007_data.name_021da2b4, native_ov007_data.name_021da474},
        {native_ov007_data.name_021da278, native_ov007_data.name_021da200, native_ov007_data.name_021da48c},
        {native_ov007_data.name_021da19c, native_ov007_data.name_021da318, native_ov007_data.name_021da4bc},
        {native_ov007_data.name_021da1b0, native_ov007_data.name_021da23c, native_ov007_data.name_021da4d4},
        {native_ov007_data.name_021da264, native_ov007_data.name_021da1c4, native_ov007_data.name_021da51c},
        {native_ov007_data.name_021da3b8, native_ov007_data.name_021da3a4, native_ov007_data.name_021da3cc},
        {native_ov007_data.name_021da37c, native_ov007_data.name_021da368, native_ov007_data.name_021da3fc},
        {native_ov007_data.name_021da340, native_ov007_data.name_021da32c, native_ov007_data.name_021da414},
        {native_ov007_data.name_021da304, native_ov007_data.name_021da1ec, native_ov007_data.name_021da4a4},
        {native_ov007_data.name_021da2c8, native_ov007_data.name_021da228, native_ov007_data.name_021da4ec},
        {native_ov007_data.name_021da28c, native_ov007_data.name_021da174, native_ov007_data.name_021da3e4},
        {native_ov007_data.name_021da250, native_ov007_data.name_021da354, native_ov007_data.name_021da42c},
        {native_ov007_data.name_021da2f0, native_ov007_data.name_021da214, native_ov007_data.name_021da504},
        {native_ov007_data.name_021da188, native_ov007_data.name_021da390, native_ov007_data.name_021da444},
        {native_ov007_data.name_021da2dc, native_ov007_data.name_021da1d8, native_ov007_data.name_021da45c},
    },
    {
        {0, 202, 148, 0, 0, 14, 85, 85, 0, {-98304, 0, 36864, -737280}, 1, 0, 0, 0, {0, 0, 0}},
        {1, 114, 122, 1, 1, 2, 17, -1, 0, {262390, 0, 201810, -286720}, 1, 0, 0, 0, {0, 0, 0}},
        {2, 162, 138, 1, 2, 1, 14, -1, 0, {26624, 0, 68608, 749568}, 1, 0, 0, 0, {0, 0, 0}},
        {3, 200, 58, 1, 3, 0, -105, -105, 0, {-94208, 0, 184320, 727040}, 1, 0, 0, 0, {0, 0, 0}},
        {4, 80, 166, 1, 4, 3, 47, -1, 0, {28959, 32768, -249446, 10240}, 1, 0, 0, 0, {0, 0, 0}},
        {5, 32, 124, 1, 5, 4, 57, -1, 0, {0, 0, 8192, 737280}, 1, 0, 0, 0, {0, 0, 0}},
        {6, 151, 38, 1, 6, 5, 37, -1, 0, {-55173, 0, 280412, 670720}, 1, 0, 0, 0, {0, 0, 0}},
        {7, 28, 100, 1, 7, 6, 67, -1, 0, {0, 0, 0, 0}, 1, 0, 0, 0, {0, 0, 0}},
        {8, 42, 56, 1, 8, 7, 79, -1, 0, {0, 0, 0, 0}, 1, 0, 0, 0, {0, 0, 0}},
        {9, 144, 76, 2, 11, 8, 1, -1, 0, {0, 0, 0, 0}, 1, 0, 0, 0, {0, 0, 0}},
        {10, 16, 42, 2, 11, 9, 2, -1, 0, {0, 0, 0, 0}, 1, 0, 0, 0, {0, 0, 0}},
        {11, 96, 40, 2, 11, 10, 3, -1, 0, {0, 0, 0, 0}, 1, 0, 0, 0, {0, 0, 0}},
        {12, 88, 98, 2, 12, 11, 4, -1, 0, {0, 0, 0, 0}, 1, 0, 0, 0, {0, 0, 0}},
        {13, 88, 122, 1, 13, 16, 24, -1, 0, {0, 0, 0, 0}, 1, 0, 0, 0, {0, 0, 0}},
        {14, 202, 148, 0, 0, 14, 85, -1, 0, {-98304, 0, 36864, -737280}, 1, 0, 0, 0, {0, 0, 0}},
        {15, 32, 28, 1, 14, 8, -120, -1, 0, {55460, 35226, 128205, -638485}, 0, 0, 0, 0, {0, 0, 0}},
    },
    "d2_ObjWorldData.bin",
    "d2_ObjWorldData.bin",
    "world.ez%c",
    "world.e",
    -1,
    {0, 0, 0},
    "world_map_sub_bg_%02d.wbg",
    "world_map_sub_bg_%02d.chr",
    "world_map_sub_bg_%02d.scrn",
};
