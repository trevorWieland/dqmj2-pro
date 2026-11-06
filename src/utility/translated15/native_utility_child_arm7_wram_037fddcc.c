typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe41c(void);
extern u32 native_utility_child_arm7_arm_037fe430(u32);
extern u32 native_utility_child_arm7_data_03805b78[];
extern u32 native_utility_child_arm7_data_03805b7c[];
u32 native_utility_child_arm7_wram_037fddcc(s32 arg0) {
    u32 temp_r0;

    temp_r0 = native_utility_child_arm7_arm_037fe41c();
    if (arg0 < (s32) *native_utility_child_arm7_data_03805b78) {
        *native_utility_child_arm7_data_03805b7c += 1;
    }
    *native_utility_child_arm7_data_03805b78 = (u32) arg0;
    native_utility_child_arm7_arm_037fe430(temp_r0);
    return *native_utility_child_arm7_data_03805b7c;
}
