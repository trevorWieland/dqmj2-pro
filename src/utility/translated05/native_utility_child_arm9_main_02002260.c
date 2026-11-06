typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_020085b4(u32);
extern u32 native_utility_child_arm9_arm_0200ab74(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02008460(void);
extern u8 native_utility_child_arm9_data_07000400[];
extern u8 native_utility_child_arm9_data_05000400[];
u32 native_utility_child_arm9_main_02002260(void) {
    native_utility_child_arm9_thumb_020085b4(0x1FFU);
    native_utility_child_arm9_arm_0200ab74(0U, 0x06800000U, 0xA4000U);
    native_utility_child_arm9_thumb_02008460();
    native_utility_child_arm9_arm_0200ab74(0xC0U, 0x07000000U, 0x400U);
    native_utility_child_arm9_arm_0200ab74(0xC0U, (u32) native_utility_child_arm9_data_07000400, 0x400U);
    native_utility_child_arm9_arm_0200ab74(0U, 0x05000000U, 0x400U);
    return native_utility_child_arm9_arm_0200ab74(0U, (u32) native_utility_child_arm9_data_05000400, 0x400U);
}
