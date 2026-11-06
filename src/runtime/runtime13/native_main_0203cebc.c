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
extern u32 native_fn_0200bd04();
extern u32 native_fn_0200bfe4();
extern u32 native_fn_0200c02c();
extern u32 native_fn_0203cd2c();
u32 native_main_0203cebc(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    u8 sp0[72];
    u32 var_r4;

    var_r4 = 0;
    native_fn_0200bd04(&sp0);
    if (native_fn_0200bfe4(&sp0, arg0) != 0) {
        var_r4 = native_fn_0203cd2c(&sp0, arg1, arg2, arg3);
        native_fn_0200c02c(&sp0);
    }
    return var_r4;
}
