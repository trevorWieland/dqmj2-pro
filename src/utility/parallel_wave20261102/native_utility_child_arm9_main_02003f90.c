typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020037dc(u32, u32, u32, u32, u32);
u32 native_utility_child_arm9_main_02003f90(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r4;

    temp_r4 = arg0 + 0x24;
    native_utility_child_arm9_arm_020037dc(arg0, 0x46524D48U, temp_r4 + 0xC, arg1, arg2);
    CHILD_FIELD(arg0, s32 *, 0x24) = (s32) CHILD_FIELD(arg0, s32 *, 0x18);
    CHILD_FIELD(temp_r4, s32 *, 4) = (s32) CHILD_FIELD(arg0, s32 *, 0x1C);
    CHILD_FIELD(temp_r4, s32 *, 8) = 0;
    return arg0;
}
