typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020062a8(u32);
extern u32 native_utility_child_arm9_arm_02006a24(u32, u32, u32);
extern u32 native_utility_child_arm9_arm_02006b44(u32, u32, u32);
extern u32 native_utility_child_arm9_arm_0200617c(u32);
u32 native_utility_child_arm9_main_02006cd4(u32 arg0, s32 arg1, u32 arg2, u32 arg3, u32 *arg4) {
    u32 temp_r0;
    u32 var_r0;

    temp_r0 = native_utility_child_arm9_arm_020062a8(arg0);
    if (temp_r0 == 0) {
        return 5U;
    }
    if (arg1 & 4) {
        if (CHILD_FIELD(temp_r0, u8 *, 3) & 1) {
            var_r0 = native_utility_child_arm9_arm_02006a24((u32) (CHILD_FIELD(temp_r0, s32 *, 0) << 8) >> 8, arg2, arg3);
        } else {
            var_r0 = native_utility_child_arm9_arm_02006b44((u32) (CHILD_FIELD(temp_r0, s32 *, 0) << 8) >> 8, arg2, arg3);
        }
        if (var_r0 == 0) {
            return 9U;
        }
        goto block_9;
    }
    var_r0 = native_utility_child_arm9_arm_0200617c((u32) (CHILD_FIELD(temp_r0, s32 *, 0) << 8) >> 8);
block_9:
    if (arg4 != 0) {
        *arg4 = var_r0;
    }
    return 0U;
}
