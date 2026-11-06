typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fe278(u32);
extern u8 native_utility_child_arm7_data_03809368[];
u32 native_utility_child_arm7_main_027e6848(void) {
    return native_utility_child_arm7_arm_037fe278((u32) native_utility_child_arm7_data_03809368);
}
