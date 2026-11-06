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
extern u32 native_fn_02008c14();
extern u32 native_fn_02049748();
extern u32 native_fn_0205f998();
u32 native_main_02048fcc(s32 arg0) {
    native_fn_02008c14(0, arg0, 0xF0);
    native_fn_02049748(arg0);
    native_fn_0205f998(arg0 + 0x18);
    native_fn_0205f998(arg0 + 0x60);
    return native_fn_0205f998(arg0 + 0xA8);
}
