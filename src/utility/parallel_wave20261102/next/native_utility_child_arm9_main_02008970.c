typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm9_data_04000008 ((volatile u16 *)0x4000008)
#define native_utility_child_arm9_data_04000000 ((volatile u32 *)0x4000000)
#define native_utility_child_arm9_data_07000000 ((volatile u8 *)0x7000000)
#define native_utility_child_arm9_data_06000000 ((volatile u8 *)0x6000000)
u32 native_utility_child_arm9_main_02008970(void) {
    return (u32) ((((s32) (*native_utility_child_arm9_data_04000008 & 0x3C) >> 2) << 0xE) + ((((u32) (*native_utility_child_arm9_data_04000000 & (s32) (u32)native_utility_child_arm9_data_07000000) >> 0x18) << 0x10) + (u32)native_utility_child_arm9_data_06000000));
}
