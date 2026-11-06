typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern const u8 *native_fn_0207d2c8(u32 key);

u32 native_main_0207d884(u32 key, const s16 *values, s32 count) {
    u32 sum;
    s32 index;
    const u8 *entry;
    s16 value;
    entry = native_fn_0207d2c8(key);
    sum = 0;
    if (key == 0) return 0;
    if (entry[3] == 3) {
        index = 0;
        if (count > 0) {
            do {
                value = values[index];
                index += 1;
                sum += (s32)value / 2;
            } while (index < count);
        }
    }
    return sum;
}
