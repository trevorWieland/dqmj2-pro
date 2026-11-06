typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm9_data_027ffdc4 ((volatile u8 *)0x27ffdc4)
u32 native_utility_child_arm9_main_0200a168(s32 arg0) {
    return *(u32 *)((arg0 * 4) + (u32)native_utility_child_arm9_data_027ffdc4);
}
