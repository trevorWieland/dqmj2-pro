typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037f8358(u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_03803ce0(u32);
extern u32 native_utility_child_arm7_data_038081b0[];
extern u32 native_utility_child_arm7_data_038081b4[];
extern u8 native_utility_child_arm7_data_038081b8[];
extern u8 native_utility_child_arm7_data_038081ac[];
u32 native_utility_child_arm7_wram_03803d74(u32 arg0) {
    *native_utility_child_arm7_data_038081b0 = 0;
    *native_utility_child_arm7_data_038081b4 = arg0;
    native_utility_child_arm7_thumb_037f8358((u32) native_utility_child_arm7_data_038081b8, 0U, 0xA4U);
    native_utility_child_arm7_thumb_03803ce0(arg0);
    *native_utility_child_arm7_data_038081ac = 3;
    return (u32) native_utility_child_arm7_data_038081ac;
}
