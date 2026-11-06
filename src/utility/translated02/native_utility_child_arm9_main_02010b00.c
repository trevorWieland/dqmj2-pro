typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02010b24(u32, u32, u32, u32);
u32 native_utility_child_arm9_main_02010b00(u32 arg0, u32 arg1, u32 arg2) {
    u16 sp0;

    sp0 = 0;
    native_utility_child_arm9_thumb_02010b24(arg0, (u32) &sp0, arg1, arg2);
    return (u32) sp0;
}
