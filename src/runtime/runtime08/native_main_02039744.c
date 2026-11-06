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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02038d60();
extern u32 native_fn_0203917c();
extern u32 native_fn_020391a4();
u32 native_main_02039744(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r4;
    u32 temp_r5;

    if (arg1 == 0) {
        return arg0;
    }
    temp_r5 = native_fn_02007ff4();
    temp_r4 = native_fn_02038d60(arg1);
    if (arg0 == native_fn_0203917c(arg2)) {
        native_fn_020391a4(arg2, 0);
    }
    native_fn_02038d60(temp_r4);
    return native_fn_02008008(temp_r5);
}
