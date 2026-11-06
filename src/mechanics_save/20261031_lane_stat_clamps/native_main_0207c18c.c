typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern s32 native_fn_0207c2b8(const u8 *, const u8 *);

u32 native_main_0207c18c(u8 *record, const u8 *features) {
    s32 maximum;
    s32 current;
    maximum = native_fn_0207c2b8(record, features);
    if (*(s16 *)(record + 4) > maximum)
        *(s16 *)(record + 4) = (s16)maximum;
    current = *(s16 *)(record + 4);
    if (current > maximum) current = maximum;
    return (u32)current;
}
