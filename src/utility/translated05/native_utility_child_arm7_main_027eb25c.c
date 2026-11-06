typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e958c(u32, u32, u32);
extern u8 native_utility_child_arm7_data_04805f80[];
extern u8 native_utility_child_arm7_data_04805fa0[];
extern u8 native_utility_child_arm7_data_04805fc0[];
extern u8 native_utility_child_arm7_data_04805fe0[];
u32 native_utility_child_arm7_main_027eb25c(u32 arg0) {
    native_utility_child_arm7_arm_027e958c((u32) native_utility_child_arm7_data_04805f80, arg0, 0x14U);
    native_utility_child_arm7_arm_027e958c((u32) native_utility_child_arm7_data_04805fa0, arg0 + 0x14, 0x14U);
    native_utility_child_arm7_arm_027e958c((u32) native_utility_child_arm7_data_04805fc0, arg0 + 0x28, 0x14U);
    native_utility_child_arm7_arm_027e958c((u32) native_utility_child_arm7_data_04805fe0, arg0 + 0x3C, 0x14U);
    return 0U;
}
