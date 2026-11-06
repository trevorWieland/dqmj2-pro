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
extern u32 native_fn_020a8640();
extern u32 native_fn_020a8720();
u32 native_main_020a8828(u32 arg0) {
    s32 var_r4;
    u32 var_r0;

    var_r0 = native_fn_020a8640();
    var_r4 = var_r0 - 1;
    if (var_r4 >= 0) {
        do {
            var_r0 = native_fn_020a8720(arg0, var_r4);
            var_r4 -= 1;
        } while (var_r4 >= 0);
    }
    return var_r0;
}
