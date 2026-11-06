typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_037ff448(u32, u32, u32);
extern u32 native_utility_child_arm7_thumb_038018d0(void);
extern u8 native_utility_child_arm7_data_03807324[];
extern u8 native_utility_child_arm7_data_03807344[];
extern u32 native_utility_child_arm7_data_038061a0[];
u32 native_utility_child_arm7_wram_03801bf8(void) {
    native_utility_child_arm7_thumb_037ff448((u32) native_utility_child_arm7_data_03807324, (u32) native_utility_child_arm7_data_03807344, 8U);
    native_utility_child_arm7_thumb_038018d0();
    *native_utility_child_arm7_data_038061a0 = 0;
    return (u32) native_utility_child_arm7_data_038061a0;
}
