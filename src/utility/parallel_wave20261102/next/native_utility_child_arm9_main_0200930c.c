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
extern u32 native_utility_child_arm9_arm_0200a68c(u32);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
u32 native_utility_child_arm9_main_0200930c(s32 arg0, void *arg1, s32 (*arg2)(), s32 arg3) {
    u32 var_r7;

    if (arg0 != CHILD_FIELD(arg1, u16 *, 4)) {
        return -2U;
    }
    if (arg3 != 0) {
        var_r7 = native_utility_child_arm9_arm_0200a678();
    } else {
        var_r7 = native_utility_child_arm9_arm_0200a64c();
    }
    CHILD_FIELD(arg1, u16 *, 4) = 0U;
    if (arg2 != 0) {
        arg2();
    }
    CHILD_FIELD(arg1, s32 *, 0) = 0;
    if (arg3 != 0) {
        native_utility_child_arm9_arm_0200a68c(var_r7);
    } else {
        native_utility_child_arm9_arm_0200a660(var_r7);
    }
    return 0U;
}
