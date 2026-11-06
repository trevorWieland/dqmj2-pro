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
extern u32 native_fn_020053a8();
extern u32 native_fn_020053c0();
extern u32 native_fn_02005424();
u32 native_main_0203c314(u32 arg0, u32 arg1, u32 arg2) {
    native_fn_020053a8();
    native_fn_020053c0(arg0, arg1, arg2);
    return native_fn_02005424();
}
