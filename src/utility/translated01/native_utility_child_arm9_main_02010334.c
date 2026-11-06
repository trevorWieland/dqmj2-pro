typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u8 native_utility_child_arm9_data_0202cc94[];
extern u8 native_utility_child_arm9_data_020103b5[];
u32 native_utility_child_arm9_main_02010334(s32 arg0) {
    return ((u32 (*)(u8 *, s32)) native_utility_child_arm9_data_020103b5)(native_utility_child_arm9_data_0202cc94, arg0);
}
