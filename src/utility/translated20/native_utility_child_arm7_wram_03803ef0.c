typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm7_thumb_03803dac(void);
#define native_utility_child_arm7_data_0380fff8 ((volatile u32 *)0x380fff8)
#define native_utility_child_arm7_data_04000214 ((volatile u32 *)0x4000214)
u32 native_utility_child_arm7_wram_03803ef0(void) {
    native_utility_child_arm7_thumb_03803dac();
    *native_utility_child_arm7_data_0380fff8 |= 0x40;
    *native_utility_child_arm7_data_04000214 = 0x40;
    return (u32) native_utility_child_arm7_data_04000214;
}
