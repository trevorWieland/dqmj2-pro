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
extern u32 native_utility_child_arm9_thumb_02002abc(u32);
u32 native_utility_child_arm9_main_02002edc(void *arg0) {
    if (M2C_FIELD(arg0, u16 *, 2) != 0) {
        native_utility_child_arm9_thumb_02002ab0(9U);
        return native_utility_child_arm9_thumb_02002abc((u32) M2C_FIELD(arg0, u16 *, 2));
    }
    return native_utility_child_arm9_thumb_02002ab0(1U);
}
