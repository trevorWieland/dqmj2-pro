typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0207b674(s32, const u8 *);
extern u32 native_fn_0206259c(void);
extern const u8 *native_fn_02065d88(s32);

u32 native_main_0207c424(const u8 *record, const u8 *features) {
    s32 total;
    total = *(const s16 *)(record + 8);
    total += native_fn_0207b674(0x94, features) * 3;
    total += native_fn_0207b674(0x95, features) * 5;
    total += native_fn_0207b674(0x96, features) * 10;
    total += native_fn_0207b674(0x97, features) * 12;
    total += native_fn_0207b674(0x98, features) * 15;
    total += native_fn_0207b674(0x99, features) * 18;
    total += native_fn_0207b674(0x9a, features) * 21;
    total += native_fn_0207b674(0x9b, features) * 24;
    total += native_fn_0207b674(0x9c, features) * 27;
    total += native_fn_0207b674(0x9d, features) * 30;
    if (native_fn_0206259c())
        total += *(const u16 *)(native_fn_02065d88(record[0x11]) + 0x1C);
    if (total >= 9999) total = 9999;
    return (u32)total;
}
