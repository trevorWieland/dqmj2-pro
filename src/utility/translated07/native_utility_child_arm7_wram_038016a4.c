typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037f8290(u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_037fee78(u32);
extern u32 native_utility_child_arm7_thumb_037ff818(u32);
extern u8 native_utility_child_arm7_data_038061a4[];
u32 native_utility_child_arm7_wram_038016a4(u32 arg0) {
    u32 temp_r0;
    u32 var_r4;

    native_utility_child_arm7_thumb_037f8290((u32) native_utility_child_arm7_data_038061a4, arg0, 0x1180U);
    M2C_FIELD(arg0, u8 **, 0x11C0) = native_utility_child_arm7_data_038061a4;
    var_r4 = 0;
    do {
        M2C_FIELD((arg0 + (var_r4 * 4)), u32 *, 0x1180) = native_utility_child_arm7_thumb_037fee78(var_r4);
        var_r4 += 1;
    } while ((s32) var_r4 < 0x10);
    temp_r0 = native_utility_child_arm7_thumb_037ff818(0U);
    M2C_FIELD(arg0, u32 *, 0x11C4) = temp_r0;
    return temp_r0;
}
