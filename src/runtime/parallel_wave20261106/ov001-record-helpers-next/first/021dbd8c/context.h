typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Object440 {
    u8 unknown0[0x1e8];
    u8 *child1e8;
    u8 bytes1ec[0x34];
    s16 field220;
    s16 field222;
    u8 unknown224[0x238 - 0x224];
    s8 field238;
    u8 unknown239[0x440 - 0x239];
} Object440;
#define MINIMUM(a,b) ((a) < (b) ? (a) : (b))
#define MAXIMUM(a,b) ((a) > (b) ? (a) : (b))
extern s32 native_fn_0207c424(u8 *, u8 *);
extern s32 native_fn_0207c52c(u8 *, u8 *);
extern s32 native_fn_ov001_021dbc64(Object440 *, s32, s32);
s32 native_ov001_021dbd8c(Object440 *);
