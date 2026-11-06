typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e8e34(u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027e8e88(void) {
    s32 temp_r4;

    temp_r4 = *native_utility_child_arm7_data_0380fff4 + 0x17C;
    native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x18);
    native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x24);
    native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x30);
    native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x3C);
    native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x48);
    native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x54);
    native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x60);
    return native_utility_child_arm7_arm_027e8e34(temp_r4 + 0x6C);
}
