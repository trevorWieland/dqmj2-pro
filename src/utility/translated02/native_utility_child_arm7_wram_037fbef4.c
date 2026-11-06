typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_arm_037fbf54(u32, u32, u32, u32);
extern u8 native_utility_child_arm7_data_027fffe8[];
extern u8 native_utility_child_arm7_data_037fbef0[];
u32 native_utility_child_arm7_wram_037fbef4(u32 arg0) {
    return native_utility_child_arm7_arm_037fbf54(arg0, (u32) native_utility_child_arm7_data_027fffe8, (u32) native_utility_child_arm7_data_037fbef0, 1U);
}
