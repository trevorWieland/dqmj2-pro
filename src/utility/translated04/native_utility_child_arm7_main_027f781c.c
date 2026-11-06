typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027f774c(u32);
extern u32 native_utility_child_arm7_arm_027f73cc(u32, u32, u32, u32);
u32 native_utility_child_arm7_main_027f781c(u32 arg0) {
    u16 sp0;

    native_utility_child_arm7_arm_027f774c((u32) &sp0);
    if (((u32) (sp0 << 0x19) >> 0x1F) == 0) {
        return 0U;
    }
    native_utility_child_arm7_arm_027f73cc(0x86U, 0x50U, arg0, 3U);
    return 1U;
}
