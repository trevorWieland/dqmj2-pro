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
extern u32 native_fn_020b45b0();
extern u32 native_fn_020b4634();
extern u32 native_fn_020b465c();
u32 native_main_020b4dbc(u32 arg0, u32 arg1, s32 arg2) {
    if (arg2 != 2) {
        if (native_fn_020b4634() != 0) {
            return 1U;
        }
        return 0U;
    }
    if (native_fn_020b465c(arg0, native_fn_020b45b0(arg1, 0)) != 0) {
        return 1U;
    }
    return 0U;
}
