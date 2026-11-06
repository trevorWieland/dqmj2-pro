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
extern u32 native_fn_0200bd2c();
u32 native_main_0200beec(u32 arg0, u32 arg1) {
    u8 sp0[72];

    native_fn_0200bd04(&sp0);
    if (native_fn_0200bd2c(&sp0, arg1, arg0, 0) != 0) {
        return 1U;
    }
    return 0U;
}
