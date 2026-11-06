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
extern u32 native_fn_02061c1c();
extern u32 native_fn_0206dfd4();
u32 native_main_0207a328(void) {
    native_fn_0206dfd4();
    native_fn_02061c1c(6, 2, 2, 0x10, 2, 0, 0);
    native_fn_02061c1c(7, 0x12, 2, 8, 2, 0, 0);
    native_fn_02061c1c(8, 2, 5, 0x16, 2, 0, 0);
    native_fn_02061c1c(9, 2, 9, 0x16, 8, 0, 0);
    return native_fn_02061c1c(0xA, 0x1D, 2, 2, 2, 0, 0);
}
