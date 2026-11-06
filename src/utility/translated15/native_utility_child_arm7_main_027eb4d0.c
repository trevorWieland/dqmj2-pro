typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027ea1e0(u32, u32);
extern u32 native_utility_child_arm7_data_0380fff4[];
extern u8 native_utility_child_arm7_data_04808018[];
u32 native_utility_child_arm7_main_027eb4d0(u16 *arg0) {
    if (*arg0 & 1) {
        return 5U;
    }
    native_utility_child_arm7_arm_027ea1e0(*native_utility_child_arm7_data_0380fff4 + 0x324, (u32) arg0);
    native_utility_child_arm7_arm_027ea1e0((u32) native_utility_child_arm7_data_04808018, (u32) arg0);
    M2C_FIELD(*native_utility_child_arm7_data_0380fff4, s32 *, 0x340) = (s32) (M2C_FIELD(*native_utility_child_arm7_data_0380fff4, s32 *, 0x340) | 2);
    return 0U;
}
