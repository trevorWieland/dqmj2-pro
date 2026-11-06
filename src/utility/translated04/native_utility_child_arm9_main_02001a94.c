typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_020085c8(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_0200aaa8(u32, u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02008dc4(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02008e0c(u32, u32, u32);
extern u8 native_utility_child_arm9_data_020266e0[];
extern u8 native_utility_child_arm9_data_020266c0[];
u32 native_utility_child_arm9_main_02001a94(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    native_utility_child_arm9_thumb_020085c8(0x20U, arg1, arg2, arg3);
    *(s32 *)0x04000000 &= 0xFFCFFFEF;
    native_utility_child_arm9_thumb_0200aaa8(3U, (u32) native_utility_child_arm9_data_020266e0, 0xC0U, 0x04000000U >> 0x10);
    native_utility_child_arm9_thumb_02008dc4(M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_020266c0, void **, 0x14), u32 *, 0x14), 0U, 0x4000U);
    return native_utility_child_arm9_thumb_02008e0c(M2C_FIELD(M2C_FIELD(native_utility_child_arm9_data_020266c0, void **, 8), u32 *, 0xC), 0U, 0x200U);
}
