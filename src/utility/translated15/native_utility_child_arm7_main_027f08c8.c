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
extern u32 native_utility_child_arm7_arm_027e9cec(void);
extern u32 native_utility_child_arm7_arm_027ea160(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027f08c8(u32 arg0, u32 arg1) {
    native_utility_child_arm7_arm_037fe6d4(0U, arg0, 0x2CU);
    M2C_FIELD(arg0, s16 *, 0x10) = (s16) native_utility_child_arm7_arm_027e9cec();
    return native_utility_child_arm7_arm_027ea160(arg0 + 0x18, arg1, *native_utility_child_arm7_data_0380fff4 + 0x324, *native_utility_child_arm7_data_0380fff4 + 0x3A8);
}
