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
extern u32 native_fn_02045ed0();
extern u32 native_fn_02061c1c();
u32 native_main_0206fc8c(void) {
    native_fn_02061c1c(6, 2, 8, 0xF, 2, 0, 0);
    native_fn_02061c1c(7, 2, 0xB, 6, 2, 0, 0);
    native_fn_02061c1c(8, 3, 0xD, 0xD, 2, 0, 0);
    native_fn_02061c1c(9, 3, 0xF, 0xD, 2, 0, 0);
    native_fn_02061c1c(0xA, 3, 0x11, 0xD, 2, 0, 0);
    native_fn_02061c1c(0xB, 3, 0x13, 0xD, 2, 0, 0);
    native_fn_02061c1c(0xC, 3, 0x15, 0xD, 2, 0, 0);
    native_fn_02061c1c(0xD, 0x16, 8, 6, 2, 0, 0);
    return native_fn_02045ed0(1);
}
