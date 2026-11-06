typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02007a68(u32, u32, u32);
extern u32 native_utility_child_arm9_thumb_02010b94(u32, u32, u32);
u32 native_utility_child_arm9_main_02007b08(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    if (native_utility_child_arm9_thumb_02007a68(arg1, arg2, arg3) == 0) {
        return 0U;
    }
    if (native_utility_child_arm9_thumb_02010b94(arg0, arg3, arg2) == 0) {
        return 1U;
    }
    return 0U;
}
