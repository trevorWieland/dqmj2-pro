typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u64 native_utility_child_arm7_divpair_arm_03805184(u32, u32);
u32 native_utility_child_arm7_main_027f6a48(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r4;
    u32 temp_r5;
    u32 var_r7;
    u32 var_r8;

    var_r8 = arg0;
    var_r7 = arg1;
    if ((u32) (var_r7 - 1) <= 1U) {
        var_r8 -= 1;
        var_r7 += 0xC;
    }
    temp_r5 = native_utility_child_arm7_divpair_arm_03805184(var_r8, 0x190U);
    temp_r4 = native_utility_child_arm7_divpair_arm_03805184(var_r8, 0x64U);
    return (u32) (native_utility_child_arm7_divpair_arm_03805184(arg2 + (temp_r5 + ((var_r8 + (var_r8 >> 2)) - temp_r4) + (u32) native_utility_child_arm7_divpair_arm_03805184((var_r7 * 0xD) + 8, 5U)), 7U) >> 32);
}
