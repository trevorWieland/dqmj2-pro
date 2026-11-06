typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02003a34(u32, u32, u32);
extern u32 native_utility_child_arm9_arm_02003978(u32, u32, u32);
u32 native_utility_child_arm9_main_020038f8(u32 arg0, s32 arg1, s32 arg2) {
    s32 var_r1;
    u32 temp_r1;

    var_r1 = arg1;
    if (var_r1 == 0) {
        var_r1 = 1;
    }
    temp_r1 = (var_r1 + 3) & ~3;
    if (arg2 >= 0) {
        return native_utility_child_arm9_arm_02003a34(arg0, temp_r1, (u32) arg2);
    }
    return native_utility_child_arm9_arm_02003978(arg0, temp_r1, 0 - arg2);
}
