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
extern u32 native_fn_02038d78();
extern u32 native_fn_0203917c();
extern u32 native_fn_020391a4();
extern u32 native_fn_02039458();
extern u32 native_fn_020397f4();
u32 native_main_020395d0(u32 arg0, s32 arg1, s32 arg2) {
    u32 var_r2;
    u32 var_r4;

    var_r4 = native_fn_0203917c();
    if (var_r4 == 0) {
        if (arg2 == 0) {
            var_r2 = 0;
        } else {
            var_r2 = native_fn_02038d78();
        }
        var_r4 = native_fn_02039458(arg0, native_fn_020397f4, var_r2, arg0, arg1);
        if ((arg2 != 0) && (var_r4 != 0)) {
            native_fn_020391a4(arg0, var_r4);
        }
    }
    return var_r4;
}
