typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))

u32 native_utility_child_arm9_main_0200c238(void *arg0, s32 arg1, s32 arg2) {
    s32 var_r1;
    s32 var_r2;

    var_r1 = arg1;
    var_r2 = arg2;
    if (var_r2 == 0) {
        var_r1 = 0;
    } else if (var_r1 == 0) {
        var_r2 = 0;
    }
    M2C_FIELD(arg0, s32 *, 0x54) = var_r1;
    M2C_FIELD(arg0, s32 *, 0x58) = var_r2;
    return (u32) arg0;
}
