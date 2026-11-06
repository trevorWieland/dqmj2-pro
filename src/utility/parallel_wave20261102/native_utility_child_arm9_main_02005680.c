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
#define native_utility_child_arm9_data_02027d40 ((volatile u8 *)0x2027d40)
u32 native_utility_child_arm9_main_02005680(u32 arg0) {
    u32 var_r1;

    var_r1 = native_utility_child_arm9_arm_020035d0((u32) native_utility_child_arm9_data_02027d40, 0U);
    if (var_r1 != 0) {
loop_2:
        if ((u32) CHILD_FIELD(arg0, u8 *, 0x3D) >= (u32) CHILD_FIELD(var_r1, u8 *, 0x3D)) {
            var_r1 = native_utility_child_arm9_arm_020035d0((u32) native_utility_child_arm9_data_02027d40, var_r1);
            if (var_r1 != 0) {
                goto loop_2;
            }
        }
    }
    return native_utility_child_arm9_arm_02003650((u32) native_utility_child_arm9_data_02027d40, var_r1, (u32) arg0);
}
