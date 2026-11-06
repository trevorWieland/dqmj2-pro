typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u16 native_utility_child_arm7_data_04808040[];
u32 native_utility_child_arm7_main_027ea5d8(u16 arg0) {
    *native_utility_child_arm7_data_04808040 = arg0;
    return 0U;
}
