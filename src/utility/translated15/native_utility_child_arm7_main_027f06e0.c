typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027e94e8(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
u32 native_utility_child_arm7_main_027f06e0(u32 arg0) {
    native_utility_child_arm7_arm_027e94e8(arg0, 3U);
    native_utility_child_arm7_arm_027e94e8(arg0 + 1, 1U);
    native_utility_child_arm7_arm_027e94e8(arg0 + 2, (u32) (u8) M2C_FIELD(*native_utility_child_arm7_data_0380fff4, u16 *, 0x3BE));
    return 3U;
}
