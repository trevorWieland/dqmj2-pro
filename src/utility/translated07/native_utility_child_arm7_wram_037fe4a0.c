typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe4f4(u32);
extern u32 native_utility_child_arm7_arm_037fbcc4(u32);
extern u32 native_utility_child_arm7_arm_037fbc1c(u32);
extern u32 native_utility_child_arm7_arm_037fe500(void);
extern u32 native_utility_child_arm7_arm_037fe50c(u32);
extern u32 native_utility_child_arm7_arm_03805624(void);
u32 native_utility_child_arm7_wram_037fe4a0(void) {
    native_utility_child_arm7_arm_037fe4f4(0U);
    native_utility_child_arm7_arm_037fe4f4(1U);
    native_utility_child_arm7_arm_037fe4f4(2U);
    native_utility_child_arm7_arm_037fe4f4(3U);
    native_utility_child_arm7_arm_037fbcc4(0x40000U);
    native_utility_child_arm7_arm_037fbc1c(-1U);
    native_utility_child_arm7_arm_037fe500();
    native_utility_child_arm7_arm_037fe50c(0x10U);
    return native_utility_child_arm7_arm_03805624();
}
