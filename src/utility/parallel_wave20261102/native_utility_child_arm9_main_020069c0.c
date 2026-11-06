typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_020063e4(u32);
extern u32 native_utility_child_arm9_arm_0200617c(u32);
extern u32 native_utility_child_arm9_arm_02006160(u32, u32);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
u32 native_utility_child_arm9_main_020069c0(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r5;
    u32 temp_r4;

    if (arg1 == 0) {
        return arg0;
    }
    temp_r4 = native_utility_child_arm9_arm_0200a64c();
    temp_r5 = native_utility_child_arm9_arm_020063e4(arg1);
    if (arg0 == native_utility_child_arm9_arm_0200617c(arg2)) {
        native_utility_child_arm9_arm_02006160(arg2, 0U);
    }
    native_utility_child_arm9_arm_020063e4(temp_r5);
    return native_utility_child_arm9_arm_0200a660(temp_r4);
}
