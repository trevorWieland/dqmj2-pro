typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u16 native_utility_child_arm7_data_04000208[];
extern u8 native_utility_child_arm7_data_038055b0[];
u32 native_utility_child_arm7_wram_03805624(void) {
    *native_utility_child_arm7_data_04000208 = 0;
    return ((u32 (*)()) native_utility_child_arm7_data_038055b0)();
}
