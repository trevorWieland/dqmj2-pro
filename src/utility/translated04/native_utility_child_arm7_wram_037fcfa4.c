typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm7_data_027f9e58[];
extern u8 native_utility_child_arm7_data_03809390[];
u32 native_utility_child_arm7_wram_037fcfa4(s32 arg0) {
    u8 *var_r0;
    u8 *var_r0_2;

    switch (arg0) {
    case 1:
        return (u32) native_utility_child_arm7_data_027f9e58;
    case 7:
        var_r0 = native_utility_child_arm7_data_03809390;
        if ((u32) native_utility_child_arm7_data_03809390 > 0x03800000U) {
            var_r0 = (u8 *)0x03800000;
        }
        return (u32) var_r0;
    case 8:
        var_r0_2 = (u8 *)0x03800000;
        if ((u32) native_utility_child_arm7_data_03809390 > 0x03800000U) {
            var_r0_2 = native_utility_child_arm7_data_03809390;
        }
        return (u32) var_r0_2;
    default:
        return 0U;
    }
}
