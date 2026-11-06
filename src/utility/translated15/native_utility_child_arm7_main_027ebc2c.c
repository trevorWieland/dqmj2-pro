typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_027f1d44(u32);
extern u16 native_utility_child_arm7_data_04808098[];
u32 native_utility_child_arm7_main_027ebc2c(void *arg0) {
    u16 *temp_r2;

    if (M2C_FIELD(arg0, u16 *, 0) != 0) {
        temp_r2 = M2C_FIELD(arg0, u16 **, 8);
        if ((*temp_r2 & 1) && ((((u32) ((s32) temp_r2 & 0x3FFF) >> 1) | 0x8000) != *native_utility_child_arm7_data_04808098)) {
            native_utility_child_arm7_arm_027f1d44((u32) arg0);
            return 1U;
        }
    }
    return 0U;
}
