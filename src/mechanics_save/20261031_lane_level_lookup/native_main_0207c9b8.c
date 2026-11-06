typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern const s32 *native_fn_0207c948(u32);
extern u32 native_fn_020630b0(u32);

u32 native_main_0207c9b8(u32 table, u32 ordinal) {
    const s32 *entries;
    u32 result;
    result = 0;
    if (ordinal - 1 <= 99) {
        entries = native_fn_0207c948(table);
        if (entries) result = (u32)entries[ordinal - 1];
    }
    return result;
}
