typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02005648(u32);
extern u32 native_utility_child_arm9_arm_02007478(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_arm_02005498(u32, u32);
u32 native_utility_child_arm9_main_020057d0(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    if (arg0 == 0) {
        return (u32) arg0;
    }
    if (CHILD_FIELD(arg0, u8 *, 0x2C) == 0) {
        return (u32) arg0;
    }
    if (arg1 == 0) {
        return native_utility_child_arm9_arm_02005648((u32) arg0);
    }
    native_utility_child_arm9_arm_02007478((u32) (arg0 + 0x1C), 0U, arg1, arg3);
    native_utility_child_arm9_arm_02005498((u32) arg0, 0U);
    CHILD_FIELD(arg0, u8 *, 0x2C) = 2U;
    return 2U;
}
