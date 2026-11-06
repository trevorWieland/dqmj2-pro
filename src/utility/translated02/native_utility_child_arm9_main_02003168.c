typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02002ab0(u32);
extern u32 native_utility_child_arm9_thumb_0200e1e4(u32);
extern u32 native_utility_child_arm9_thumb_02002efd(u32);
u32 native_utility_child_arm9_main_02003168(void) {
    native_utility_child_arm9_thumb_02002ab0(3U);
    if (native_utility_child_arm9_thumb_0200e1e4((u32) native_utility_child_arm9_thumb_02002efd) != 2) {
        native_utility_child_arm9_thumb_02002ab0(9U);
        return 0U;
    }
    return 1U;
}
