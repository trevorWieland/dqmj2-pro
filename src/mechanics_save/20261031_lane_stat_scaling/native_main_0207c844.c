typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0207c2b8(const u8 *, const u8 *);
u32 native_main_0207c844(u8 *record, u32 scale, const u8 *features) {
    s32 maximum;
    u32 product;
    maximum = native_fn_0207c2b8(record, features);
    product = (u32)maximum * scale;
    *(s16 *)(record + 4) = (s16)((s32)product / 100);
    record[0x13] = 0;
    return 0;
}
