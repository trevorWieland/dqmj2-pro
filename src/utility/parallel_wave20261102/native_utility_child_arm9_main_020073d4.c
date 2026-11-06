typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define CHILD_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_020073d4(u32 arg0, s32 arg1) {
    u32 var_r0;
    s32 temp_r2;
    u32 temp_r3;

    if (arg1 < 0) {
        return 0U;
    }
    if ((u32) arg1 >= (u32) CHILD_FIELD(arg0, u32 *, 0x1C)) {
        return 0U;
    }
    temp_r2 = arg1 * 0xC;
    temp_r3 = arg0 + 0x20;
    var_r0 = temp_r3 + temp_r2;
    if (*(u32 *)(temp_r3 + temp_r2) == -1) {
        var_r0 = 0;
    }
    return (u32) var_r0;
}
