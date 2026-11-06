typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0207b674(s32, const u8 *);
extern u32 native_fn_0206259c(void);
extern const u8 *native_fn_02065d88(s32);

u32 native_main_0207c52c(const u8 *record, const u8 *features) {
    s32 total;
    total = *(const s16 *)(record + 10);
    total += native_fn_0207b674(0x9e, features) * 3;
    total += native_fn_0207b674(0x9f, features) * 5;
    total += native_fn_0207b674(0xa0, features) * 10;
    total += native_fn_0207b674(0xa1, features) * 12;
    total += native_fn_0207b674(0xa2, features) * 15;
    total += native_fn_0207b674(0xa3, features) * 18;
    total += native_fn_0207b674(0xa4, features) * 21;
    total += native_fn_0207b674(0xa5, features) * 24;
    total += native_fn_0207b674(0xa6, features) * 27;
    total += native_fn_0207b674(0xa7, features) * 30;
    if (native_fn_0206259c())
        total += native_fn_02065d88(record[0x11])[0x1e];
    if (total >= 9999) total = 9999;
    return (u32)total;
}
