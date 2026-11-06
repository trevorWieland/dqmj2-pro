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
extern u32 native_fn_0202ad78();
extern u32 native_fn_0202ada4();
extern u32 native_fn_0202b1a8();
u32 native_main_0202b4e8(s32 arg0, s32 arg1) {
    u8 sp0[8];
    s32 temp_r4;

    temp_r4 = arg1 - 0x10;
    native_fn_0202ad78(&sp0, temp_r4);
    native_fn_0202ada4(arg0 + 0x2C, temp_r4);
    return native_fn_0202b1a8(arg0 + 0x24, &sp0);
}
