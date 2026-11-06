typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020038f8(u32, u32, u32);
extern u32 native_utility_child_arm9_arm_0200ad8c(u32, u32);
extern u32 native_utility_child_arm9_data_02027c98[];
u32 native_utility_child_arm9_main_020017a0(u32 *arg0) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm9_arm_020038f8(*native_utility_child_arm9_data_02027c98, (u32) *arg0 >> 8, 4U);
    native_utility_child_arm9_arm_0200ad8c((u32) arg0, temp_r0);
    return temp_r0;
}
