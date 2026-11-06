typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_data_02028710[];
u32 native_utility_child_arm9_main_020063e4(u32 arg0) {
    u32 temp_r2;

    temp_r2 = *native_utility_child_arm9_data_02028710;
    *native_utility_child_arm9_data_02028710 = arg0;
    return temp_r2;
}
