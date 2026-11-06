typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02003f90(u32, u32, u32);
u32 native_utility_child_arm9_main_02003e34(s32 arg0, s32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 temp_r1;

    temp_r1 = (arg1 + arg0) & ~3;
    temp_r0 = (arg0 + 3) & ~3;
    if ((temp_r0 > temp_r1) || ((u32) (temp_r1 - temp_r0) < 0x30U)) {
        return 0U;
    }
    return native_utility_child_arm9_arm_02003f90(temp_r0, temp_r1, arg2);
}
