typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_0200b77c(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200b7b0(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_0200af08(u32, u32);
u32 native_utility_child_arm9_main_020068e0(u32 arg0, s32 arg1, u32 arg2, u32 arg3) {
    if (arg0 == native_utility_child_arm9_thumb_0200b77c(arg2, arg3)) {
        native_utility_child_arm9_thumb_0200b7b0(arg2, arg3, 0U);
    }
    return native_utility_child_arm9_thumb_0200af08(arg0, arg0 + arg1);
}
