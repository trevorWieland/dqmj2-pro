typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fbc50(u32);
extern u32 native_utility_child_arm7_arm_037f878c(u32, u32);
extern u32 native_utility_child_arm7_arm_037f8a10(u32, u32);
extern u32 native_utility_child_arm7_arm_037fbc8c(u32);
u32 native_utility_child_arm7_wram_037f899c(u32 arg0, u32 arg1, void *arg2) {
    u32 var_r5;
    u32 temp_r4;

    if (M2C_FIELD(arg2, u16 *, 0xA) != 0xBF1D) {
        return 1U;
    }
    temp_r4 = native_utility_child_arm7_arm_037fbc50(0x01000000U);
    var_r5 = native_utility_child_arm7_arm_037f878c(arg0, (u32) arg2);
    if (var_r5 == 0) {
        var_r5 = native_utility_child_arm7_arm_037f8a10(arg1, (u32) arg2);
    }
    native_utility_child_arm7_arm_037fbc8c(temp_r4);
    return var_r5;
}
