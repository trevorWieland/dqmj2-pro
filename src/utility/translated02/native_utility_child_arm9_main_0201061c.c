typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200f9b4(u32, u32, u32);
u32 native_utility_child_arm9_main_0201061c(u32 arg0) {
    u32 temp_r0;

    do {
        temp_r0 = native_utility_child_arm9_thumb_0200f9b4(8U, arg0, 0U);
    } while (temp_r0 != 0);
    return temp_r0;
}
