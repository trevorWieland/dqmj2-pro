typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200af60(u32, u32);
extern u32 native_utility_child_arm9_data_02027d30[];
u32 native_utility_child_arm9_main_02005468(u32 arg0) {
    if (arg0 == 0) {
        return arg0;
    }
    native_utility_child_arm9_thumb_0200af60(arg0, 0U);
    *native_utility_child_arm9_data_02027d30 &= ~arg0;
    return (u32) native_utility_child_arm9_data_02027d30;
}
