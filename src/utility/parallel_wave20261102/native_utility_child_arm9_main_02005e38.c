typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_arm_02005d50(u32);
u32 native_utility_child_arm9_main_02005e38(u32 arg0) {
    if (((s32) (CHILD_FIELD(arg0, s32 *, 0x24) << 0x1F) >> 0x1F) == 0) {
        return (u32) arg0;
    }
    return native_utility_child_arm9_arm_02005d50((u32) arg0);
}
