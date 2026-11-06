typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200abc0(u32, u32, u32);
u32 native_utility_child_arm9_main_0200c33c(u32 arg0) {
    u32 temp_r0;

    native_utility_child_arm9_arm_0200abc0(arg0, 0U, 0x5CU);
    M2C_FIELD(arg0, s32 *, 0x10) = 0;
    M2C_FIELD(arg0, s32 *, 0xC) = (s32) M2C_FIELD(arg0, s32 *, 0x10);
    M2C_FIELD(arg0, u32 *, 0x18) = 0U;
    temp_r0 = M2C_FIELD(arg0, u32 *, 0x18);
    M2C_FIELD(arg0, u32 *, 0x14) = temp_r0;
    return temp_r0;
}
