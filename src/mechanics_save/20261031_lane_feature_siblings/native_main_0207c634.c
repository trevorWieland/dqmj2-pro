typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0207b674(s32, const u8 *);
extern u32 native_fn_0206259c(void);
extern const u8 *native_fn_02065d88(s32);

u32 native_main_0207c634(const u8 *record, const u8 *features) {
    s32 total;
    total = *(const s16 *)(record + 12);
    total += native_fn_0207b674(0xa8, features) * 3;
    total += native_fn_0207b674(0xa9, features) * 5;
    total += native_fn_0207b674(0xaa, features) * 10;
    total += native_fn_0207b674(0xab, features) * 12;
    total += native_fn_0207b674(0xac, features) * 15;
    total += native_fn_0207b674(0xad, features) * 18;
    total += native_fn_0207b674(0xae, features) * 21;
    total += native_fn_0207b674(0xaf, features) * 24;
    total += native_fn_0207b674(0xb0, features) * 27;
    total += native_fn_0207b674(0xb1, features) * 30;
    if (native_fn_0206259c())
        total += native_fn_02065d88(record[0x11])[0x1f];
    if (total >= 9999) total = 9999;
    return (u32)total;
}
