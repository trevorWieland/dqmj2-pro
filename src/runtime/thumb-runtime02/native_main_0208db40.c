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
extern u32 native_fn_0208daac();
u32 native_main_0208db40(u32 arg0, s32 arg1, u32 arg2, s32 arg3, s32 arg4, s32 arg5) {
    u32 var_r0;

    var_r0 = native_fn_0208daac(arg0, arg1, arg4, arg5);
    if ((var_r0 != 0) && (arg3 != 0)) {
        var_r0 = native_fn_0208daac(arg2, arg3, arg4, 0);
    }
    return var_r0;
}
