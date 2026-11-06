typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200f8d4(void);
extern u32 native_utility_child_arm9_thumb_0200fa48(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200fa74(u32, u32);
extern u32 native_utility_child_arm9_arm_0200a6e0(u32, u32);
extern u16 native_utility_child_arm9_data_02029614[];
u32 native_utility_child_arm9_main_0200a724(void) {
    if (*native_utility_child_arm9_data_02029614 != 0) {
        return (u32) native_utility_child_arm9_data_02029614;
    }
    *native_utility_child_arm9_data_02029614 = 1;
    native_utility_child_arm9_thumb_0200f8d4();
    do {

    } while (native_utility_child_arm9_thumb_0200fa48(0xCU, 1U) == 0);
    return native_utility_child_arm9_thumb_0200fa74(0xCU, (u32) native_utility_child_arm9_arm_0200a6e0);
}
