typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_020069c0(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_0200af24(u32, u32);
extern u32 native_utility_child_arm9_thumb_0200b918(u32);
u32 native_utility_child_arm9_main_02006988(u32 arg0, s32 arg1, u32 arg2, u32 arg3) {
    native_utility_child_arm9_arm_020069c0(arg0, arg2, arg3);
    native_utility_child_arm9_thumb_0200af24(arg0, arg0 + arg1);
    return native_utility_child_arm9_thumb_0200b918(arg0);
}
