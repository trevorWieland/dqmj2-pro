typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
u32 native_main_02060a60(s32 arg0, s32 arg1, s32 arg2, s32 arg3) {
    s32 var_r0;
    s32 var_r2;

    if (arg0 == 0) {
        var_r2 = 0;
    } else if (arg0 == 1) {
        var_r2 = 1;
    } else if ((arg2 - arg0) == 1) {
        var_r2 = 3;
    } else if (arg0 == arg2) {
        var_r2 = 4;
    } else {
        var_r2 = 2;
    }
    if (arg1 == 0) {
        var_r0 = 0;
    } else if (arg1 == 1) {
        var_r0 = 1;
    } else if ((arg3 - arg1) == 1) {
        var_r0 = 3;
    } else if (arg1 == arg3) {
        var_r0 = 4;
    } else {
        var_r0 = 2;
    }
    return (u32) (s8) (var_r2 + (var_r0 * 5));
}
