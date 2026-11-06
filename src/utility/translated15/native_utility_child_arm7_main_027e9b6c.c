typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe6d4(u32, u32, u32);
extern u32 native_utility_child_arm7_arm_027f5a70(u32, u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027e9b6c(void) {
    u32 temp_r4;

    temp_r4 = *native_utility_child_arm7_data_0380fff4 + 0x5F8;
    native_utility_child_arm7_arm_037fe6d4(0U, temp_r4, 0x10U);
    native_utility_child_arm7_arm_027f5a70(0x40U, 1U, temp_r4);
    native_utility_child_arm7_arm_027f5a70(0x41U, 1U, temp_r4 + 2);
    native_utility_child_arm7_arm_027f5a70(0x42U, 1U, temp_r4 + 4);
    return native_utility_child_arm7_arm_027f5a70(0x43U, 1U, temp_r4 + 6);
}
