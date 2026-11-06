typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fbd44(u32, u32);
extern u32 native_utility_child_arm7_arm_037fbc8c(u32);
extern u32 native_utility_child_arm7_arm_037f9454(void);
u32 native_utility_child_arm7_main_027ebc00(void) {
    native_utility_child_arm7_arm_037fbd44(0x01000000U, (u32) native_utility_child_arm7_arm_037f9454);
    return native_utility_child_arm7_arm_037fbc8c(0x01000000U);
}
