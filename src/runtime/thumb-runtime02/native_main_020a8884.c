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
u32 native_main_020a8884(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 (*arg4)(s32, s32), s32 *arg5) {
    s32 sp8;
    s32 sp4;
    s32 sp0;
    s32 temp_r0;
    s32 temp_r6;
    s32 var_r4;
    s32 var_r5;

    sp0 = arg0;
    var_r4 = 0;
    sp4 = arg1;
    sp8 = arg3;
    var_r5 = arg2 - 1;
    *arg5 = 0;
    if (var_r5 >= 0) {
        do {
            temp_r6 = (s32) (var_r4 + var_r5) >> 1;
            temp_r0 = arg4(sp4 + (temp_r6 * sp8), sp0);
            if (temp_r0 == 0) {
                *arg5 = 1;
            }
            if (temp_r0 < 0) {
                var_r4 = temp_r6 + 1;
            } else {
                var_r5 = temp_r6 - 1;
            }
        } while (var_r4 <= var_r5);
    }
    return sp4 + (var_r4 * sp8);
}
