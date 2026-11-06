typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_utility_child_arm9_thumb_02010860(u32, u32, u32);
u32 native_utility_child_arm9_main_020107ac(s32 arg0, u32 arg1, u32 arg2) {
    u32 var_r0;

    switch (arg0) {
    case 1:
        var_r0 = 1;
        break;
    case 3:
        var_r0 = 2;
        break;
    case 2:
        var_r0 = 3;
        break;
    default:
        var_r0 = 0;
        break;
    }
    if (var_r0 != 0) {
        return native_utility_child_arm9_thumb_02010860(var_r0, arg1, arg2);
    }
    return 0xFFFFU;
}
