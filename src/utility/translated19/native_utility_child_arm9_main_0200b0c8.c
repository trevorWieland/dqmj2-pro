typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02009bac(void);
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
#define native_utility_child_arm9_data_04fff200 ((volatile u32 *)0x4fff200)
u32 native_utility_child_arm9_main_0200b0c8(void) {
    u32 temp_r0;
    u32 temp_r4;

    if (native_utility_child_arm9_thumb_02009bac() == 0) {
        return 1U;
    }
    temp_r0 = native_utility_child_arm9_arm_0200a64c();
    *native_utility_child_arm9_data_04fff200 = 0x10;
    temp_r4 = *native_utility_child_arm9_data_04fff200;
    native_utility_child_arm9_arm_0200a660(temp_r0);
    if (temp_r4 != 0) {
        return 1U;
    }
    return 0U;
}
