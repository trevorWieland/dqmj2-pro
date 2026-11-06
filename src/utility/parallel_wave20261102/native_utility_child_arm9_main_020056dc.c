typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020035d0(u32, u32);
extern u32 native_utility_child_arm9_arm_02003650(u32, u32, u32);
u32 native_utility_child_arm9_main_020056dc(u32 arg0, u32 arg1) {
    u32 temp_r0;
    u32 var_r1;

    var_r1 = native_utility_child_arm9_arm_020035d0(arg0, 0U);
    if (var_r1 != 0) {
loop_1:
        if ((u32) CHILD_FIELD(arg1, u8 *, 0x3D) >= (u32) CHILD_FIELD(var_r1, u8 *, 0x3D)) {
            var_r1 = native_utility_child_arm9_arm_020035d0(arg0, var_r1);
            if (var_r1 != 0) {
                goto loop_1;
            }
        }
    }
    temp_r0 = native_utility_child_arm9_arm_02003650(arg0, var_r1, (u32) arg1);
    CHILD_FIELD(arg1, u32 *, 4) = arg0;
    return temp_r0;
}
