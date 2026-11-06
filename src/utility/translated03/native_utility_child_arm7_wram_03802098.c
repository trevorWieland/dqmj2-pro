typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_0380229c(u32);
extern u32 native_utility_child_arm7_thumb_03802160(u32, u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_03802238(u32, u32);
extern u8 native_utility_child_arm7_data_038054f8[];
extern u8 native_utility_child_arm7_data_03802105[];
u32 native_utility_child_arm7_wram_03802098(void) {
    native_utility_child_arm7_thumb_0380229c(1U);
    native_utility_child_arm7_thumb_03802160((u32) native_utility_child_arm7_data_038054f8, 0U, 1U, (u32) native_utility_child_arm7_data_03802105);
    return native_utility_child_arm7_thumb_03802238(0U, 0U);
}
