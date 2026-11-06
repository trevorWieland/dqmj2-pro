typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
extern u32 native_utility_child_arm9_data_02029654[];
u32 native_utility_child_arm9_main_0200b22c(u32 arg0) {
    u32 temp_r0;
    u32 var_r4;

    temp_r0 = native_utility_child_arm9_arm_0200a64c();
    if (arg0 > (u32) *native_utility_child_arm9_data_02029654) {
        if ((u32) (arg0 - *native_utility_child_arm9_data_02029654) < 0x80000000U) {
            var_r4 = 0;
        } else {
            var_r4 = 1;
        }
    } else if ((u32) (*native_utility_child_arm9_data_02029654 - arg0) < 0x80000000U) {
        var_r4 = 1;
    } else {
        var_r4 = 0;
    }
    native_utility_child_arm9_arm_0200a660(temp_r0);
    return var_r4;
}
