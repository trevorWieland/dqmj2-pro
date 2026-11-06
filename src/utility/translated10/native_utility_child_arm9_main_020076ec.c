typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02007740(u32);
extern u32 native_utility_child_arm9_arm_0200ac54(u32, u32, u32);
u32 native_utility_child_arm9_main_020076ec(u32 arg0, u32 arg1) {
    s32 sp4;
    s32 sp0;

    if (native_utility_child_arm9_thumb_02007740(arg0) == 0) {
        return 0U;
    }
    native_utility_child_arm9_arm_0200ac54(arg0, (u32) &sp4, 4U);
    native_utility_child_arm9_arm_0200ac54(arg1, (u32) &sp0, 4U);
    if ((sp4 | sp0) == -2) {
        return 0U;
    }
    if (~sp0 & sp4) {
        return 1U;
    }
    return 0U;
}
