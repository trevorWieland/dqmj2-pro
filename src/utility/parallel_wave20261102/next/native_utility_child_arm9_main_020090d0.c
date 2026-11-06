typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define native_utility_child_arm9_data_04000208 ((volatile u16 *)0x4000208)
#define native_utility_child_arm9_data_04000210 ((volatile u32 *)0x4000210)
u32 native_utility_child_arm9_main_020090d0(u32 arg0) {
    u16 temp_r3;
    u32 temp_r1;

    temp_r3 = *native_utility_child_arm9_data_04000208;
    *native_utility_child_arm9_data_04000208 = 0;
    temp_r1 = *native_utility_child_arm9_data_04000210;
    *native_utility_child_arm9_data_04000210 = arg0;
    (void)*native_utility_child_arm9_data_04000208;
    *native_utility_child_arm9_data_04000208 = temp_r3;
    return temp_r1;
}
