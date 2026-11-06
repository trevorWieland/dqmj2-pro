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
u32 native_main_02071c9c(void) {
    native_fn_02061c1c(6, 0xA, 0xE, 0xB, 2, 0, 0);
    native_fn_02061c1c(7, 0x15, 0x13, 0xA, 2, 0, 0);
    native_fn_02061c1c(8, 0x14, 0x15, 0xB, 2, 0, 0);
    native_fn_02061c1c(9, 2, 0x13, 0xA, 2, 0, 0);
    native_fn_02061c1c(0xA, 1, 0x15, 0xB, 2, 0, 0);
    return native_fn_02045ed0(1);
}
