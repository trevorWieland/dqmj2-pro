typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020040bc(u32, u32);
u32 native_utility_child_arm9_main_0200408c(u32 arg0, s32 *arg1) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm9_arm_020040bc(arg0, 0x5343524EU);
    if (temp_r0 != 0) {
        *arg1 = temp_r0 + 8;
        return 1U;
    }
    *arg1 = 0;
    return 0U;
}
