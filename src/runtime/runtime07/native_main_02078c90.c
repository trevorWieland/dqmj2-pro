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
extern u32 native_fn_02078dd8();
extern u32 native_fn_02078e20();
extern u32 native_fn_02078e24();
extern u32 native_fn_ov000_02217a54();
u32 native_main_02078c90(void) {
    native_fn_02078e24();
    native_fn_02078dd8();
    native_fn_02078e20();
    native_fn_ov000_02217a54();
    return 0U;
}
