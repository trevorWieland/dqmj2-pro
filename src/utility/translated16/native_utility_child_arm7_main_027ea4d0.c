typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e98b4(u32);
extern u32 native_utility_child_arm7_arm_027e9cb8(u32);
extern u32 native_utility_child_arm7_arm_027e9c78(u32, u32);
extern u32 native_utility_child_arm7_arm_027e9934(void);
extern u16 native_utility_child_arm7_data_04808036[];
extern u16 native_utility_child_arm7_data_04808168[];
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027ea4d0(void) {
    u16 temp_r0;
    u32 temp_r0_2;

    *native_utility_child_arm7_data_04808036 = 0;
    native_utility_child_arm7_arm_027e98b4(8U);
    *native_utility_child_arm7_data_04808168 = 0;
    temp_r0 = M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x5F8);
    switch (temp_r0) {
    case 2:
        temp_r0_2 = native_utility_child_arm7_arm_027e9cb8(1U);
        native_utility_child_arm7_arm_027e9c78(1U, temp_r0_2 & 0x7F);
        native_utility_child_arm7_arm_027e9c78(1U, temp_r0_2);
        native_utility_child_arm7_arm_027e98b4(0x28U);
        return native_utility_child_arm7_arm_027e9934();
    case 3:
        return native_utility_child_arm7_arm_027e9934();
    default:
        return (u32) temp_r0;
    }
}
