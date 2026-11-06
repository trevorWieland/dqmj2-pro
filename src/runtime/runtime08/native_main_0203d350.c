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
extern u32 native_fn_0200eaa4();
u32 native_main_0203d350(void) {
    s32 sp0;
    u32 var_r4;

    var_r4 = 1;
    native_fn_0200eaa4(&sp0);
    if ((native_fn_0200eaa4(&sp0) == 0) && (sp0 == 1)) {
        var_r4 = 0;
    }
    return var_r4;
}
