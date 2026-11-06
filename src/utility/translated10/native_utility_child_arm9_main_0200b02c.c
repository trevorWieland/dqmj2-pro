typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200ae98(u32, u32, u32, u32, u32);
u32 native_utility_child_arm9_main_0200b02c(u32 arg0) {
    return native_utility_child_arm9_thumb_0200ae98(3U, arg0, 0U, 0U, 0U);
}
