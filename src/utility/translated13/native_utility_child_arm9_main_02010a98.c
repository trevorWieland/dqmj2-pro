typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_0200a64c(void);
extern u32 native_utility_child_arm9_arm_0200a660(u32);
extern u32 native_utility_child_arm9_data_0202cca0[];
u32 native_utility_child_arm9_main_02010a98(void) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm9_arm_0200a64c();
    if (*native_utility_child_arm9_data_0202cca0 != 0) {
        native_utility_child_arm9_arm_0200a660(temp_r0);
        return 0U;
    }
    *native_utility_child_arm9_data_0202cca0 = 1;
    native_utility_child_arm9_arm_0200a660(temp_r0);
    return 1U;
}
