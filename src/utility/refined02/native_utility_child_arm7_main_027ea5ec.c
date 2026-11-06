typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_data_0380fff4[];
extern u16 native_utility_child_arm7_data_0480803c[];
u32 native_utility_child_arm7_main_027ea5ec(u16 arg0) {
    M2C_FIELD(*native_utility_child_arm7_data_0380fff4, s16 *, 0x354) = (s16) ((u32) arg0 >> 1);
    *native_utility_child_arm7_data_0480803c = arg0;
    return 0U;
}
