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
extern u32 native_utility_child_arm9_arm_020035d0(u32, u32);
extern u32 native_utility_child_arm9_arm_020035e8(u32, u32);
extern u32 native_utility_child_arm9_arm_020070a4(u32);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
u32 native_utility_child_arm9_main_020070d8(u32 arg0, s32 arg1) {
    u32 temp_r4;
    u32 var_r5;
    u32 temp_r6;

    temp_r6 = native_utility_child_arm9_arm_0200a64c();
    var_r5 = native_utility_child_arm9_arm_020035d0(arg0, 0U);
    if (var_r5 != 0) {
        do {
            temp_r4 = native_utility_child_arm9_arm_020035d0(arg0, var_r5);
            if (M2C_FIELD(var_r5, s32 *, 8) == arg1) {
                native_utility_child_arm9_arm_020035e8(arg0, var_r5);
                native_utility_child_arm9_arm_020070a4(var_r5);
            }
            var_r5 = temp_r4;
        } while (temp_r4 != 0);
    }
    return native_utility_child_arm9_arm_0200a660(temp_r6);
}
