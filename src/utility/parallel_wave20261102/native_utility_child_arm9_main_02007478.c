typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02007444(u32, u32, u32, u32);
u32 native_utility_child_arm9_main_02007478(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    CHILD_FIELD(arg0, u32 *, 0) = native_utility_child_arm9_arm_02007444(arg0, arg1, arg2, arg3);
    CHILD_FIELD(arg0, u32 *, 4) = arg1;
    CHILD_FIELD(arg0, u32 *, 0xC) = arg2;
    CHILD_FIELD(arg0, s32 *, 8) = 0;
    return 0U;
}
