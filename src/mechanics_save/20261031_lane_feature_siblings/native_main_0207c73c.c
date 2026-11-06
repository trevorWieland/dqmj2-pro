typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0207b674(s32, const u8 *);
extern u32 native_fn_0206259c(void);
extern const u8 *native_fn_02065d88(s32);

u32 native_main_0207c73c(const u8 *record, const u8 *features) {
    s32 total;
    total = *(const s16 *)(record + 14);
    total += native_fn_0207b674(0xb2, features) * 3;
    total += native_fn_0207b674(0xb3, features) * 5;
    total += native_fn_0207b674(0xb4, features) * 10;
    total += native_fn_0207b674(0xb5, features) * 12;
    total += native_fn_0207b674(0xb6, features) * 15;
    total += native_fn_0207b674(0xb7, features) * 18;
    total += native_fn_0207b674(0xb8, features) * 21;
    total += native_fn_0207b674(0xb9, features) * 24;
    total += native_fn_0207b674(0xba, features) * 27;
    total += native_fn_0207b674(0xbb, features) * 30;
    if (native_fn_0206259c())
        total += native_fn_02065d88(record[0x11])[0x20];
    if (total >= 9999) total = 9999;
    return (u32)total;
}
