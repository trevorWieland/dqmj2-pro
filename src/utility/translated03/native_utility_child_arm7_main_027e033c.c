typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_027f84f0[];
extern u8 native_utility_child_arm7_data_027f94f0[];
u32 native_utility_child_arm7_main_027e033c(s8 arg0) {
    s32 var_r3;

    var_r3 = 0;
    do {
        M2C_FIELD(&native_utility_child_arm7_data_027f84f0[var_r3], s8 *, 0x1554) = arg0;
        var_r3 += 1;
    } while (var_r3 < 0x20);
    M2C_FIELD(native_utility_child_arm7_data_027f94f0, s32 *, 0x574) = 0;
    return (u32) native_utility_child_arm7_data_027f94f0;
}
