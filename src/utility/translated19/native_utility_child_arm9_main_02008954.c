typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm9_data_04001008 ((volatile u16 *)0x4001008)
#define native_utility_child_arm9_data_06200000 ((volatile u8 *)0x6200000)
u32 native_utility_child_arm9_main_02008954(void) {
    return (u32) ((((s32) (*native_utility_child_arm9_data_04001008 & 0x3C) >> 2) << 0xE) + native_utility_child_arm9_data_06200000);
}
