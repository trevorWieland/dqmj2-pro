typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fb8cc(void);
extern u16 native_utility_child_arm7_data_0480815a[];
extern u16 native_utility_child_arm7_data_04808158[];
u32 native_utility_child_arm7_main_027e9c78(s32 arg0, u16 arg1) {
    *native_utility_child_arm7_data_0480815a = arg1;
    *native_utility_child_arm7_data_04808158 = arg0 | 0x5000;
    if (native_utility_child_arm7_arm_037fb8cc() != 0) {
        return -1U;
    }
    return 0U;
}
