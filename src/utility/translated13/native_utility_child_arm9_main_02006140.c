typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_data_02028698[];
extern u32 native_utility_child_arm9_data_020286bc[];
u32 native_utility_child_arm9_main_02006140(void) {
    *native_utility_child_arm9_data_02028698 = 0;
    *native_utility_child_arm9_data_020286bc = 0;
    return (u32) native_utility_child_arm9_data_020286bc;
}
