typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e9f20(void);
extern u32 native_utility_child_arm7_arm_037fe708(u32, u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027ea124(void) {
    native_utility_child_arm7_arm_027e9f20();
    return native_utility_child_arm7_arm_037fe708(0U, *native_utility_child_arm7_data_0380fff4 + 0x53C, 0xB4U);
}
