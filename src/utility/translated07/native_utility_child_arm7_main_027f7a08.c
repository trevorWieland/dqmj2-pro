typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027f73b4(u32);
extern u32 native_utility_child_arm7_arm_027f73cc(u32, u32, u32, u32);
u32 native_utility_child_arm7_main_027f7a08(u32 arg0) {
    native_utility_child_arm7_arm_027f73b4(0x8000U);
    return native_utility_child_arm7_arm_027f73cc(0x86U, 0x20U, arg0, 4U);
}
