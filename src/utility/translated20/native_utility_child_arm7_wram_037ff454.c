typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037ff488(u32, u32, u32, u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_037ff494(u32);
#define native_utility_child_arm7_data_03805cd8 ((volatile u8 *)0x3805cd8)
extern u8 native_utility_child_arm7_data_037ff319[];
#define native_utility_child_arm7_data_0380617c ((volatile u8 *)0x380617c)
u32 native_utility_child_arm7_wram_037ff454(u32 arg0) {
    native_utility_child_arm7_thumb_037ff488((u32) native_utility_child_arm7_data_03805cd8, (u32) native_utility_child_arm7_data_037ff319, 0U, (u32) native_utility_child_arm7_data_0380617c, 0x400U, arg0);
    return native_utility_child_arm7_thumb_037ff494((u32) native_utility_child_arm7_data_03805cd8);
}
