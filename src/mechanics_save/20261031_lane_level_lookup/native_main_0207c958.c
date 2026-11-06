typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
extern const s32 *native_fn_0207c948(u32);
extern u32 native_fn_020630b0(u32);

u32 native_main_0207c958(u32 table, s32 value, u32 capWord) {
    const s32 *entries;
    u32 result;
    s32 index;
    u32 maximum;
    result = 0;
    entries = native_fn_0207c948(table);
    if (entries) {
        index = 0;
        do {
            if (value < entries[index]) {
                result = (u8)index;
                break;
            }
            if (index == 99) result = 100;
            index += 1;
        } while (index < 100);
    }
    maximum = native_fn_020630b0(capWord);
    if (result > maximum) result = maximum;
    return result;
}
