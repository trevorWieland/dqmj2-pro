typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_data_038061a0[];
u32 native_utility_child_arm7_wram_03801508(s32 arg0, s16 arg1) {
    M2C_FIELD((*native_utility_child_arm7_data_038061a0 + (arg0 * 2)), s16 *, 0x260) = arg1;
    return 0x260U;
}
