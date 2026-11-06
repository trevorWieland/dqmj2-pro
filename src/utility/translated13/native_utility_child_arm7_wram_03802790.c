typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_data_04000214[];
extern u32 native_utility_child_arm7_data_03807be8[];
u32 native_utility_child_arm7_wram_03802790(void) {
    u32 var_r0;

    var_r0 = 1;
    if (*native_utility_child_arm7_data_04000214 & 0x100000) {
        var_r0 = 0;
        *native_utility_child_arm7_data_03807be8 = 1;
    }
    return var_r0;
}
