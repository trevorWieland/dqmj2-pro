typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a678(void);
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_0200ad84(u32, u32);
extern u32 native_utility_child_arm9_arm_0200a68c(u32);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
u32 native_utility_child_arm9_main_020092ac(u32 arg0, u32 arg1, s32 (*arg2)(), s32 arg3) {
    u32 temp_r0;
    u32 sp4;
    u32 sp0;

    if (arg3 != 0) {
        sp0 = native_utility_child_arm9_arm_0200a678();
    } else {
        sp0 = native_utility_child_arm9_arm_0200a64c();
    }
    temp_r0 = native_utility_child_arm9_arm_0200ad84(arg0, arg1);
    sp4 = temp_r0;
    if (temp_r0 == 0) {
        if (arg2 != 0) {
            arg2();
        }
        CHILD_FIELD(arg1, s16 *, 4) = (s16) arg0;
    }
    if (arg3 != 0) {
        native_utility_child_arm9_arm_0200a68c(sp0);
    } else {
        native_utility_child_arm9_arm_0200a660(sp0);
    }
    return sp4;
}
