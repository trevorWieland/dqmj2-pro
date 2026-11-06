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
extern u32 native_fn_02008be0();
extern u32 native_fn_020d3b7c();
extern u8 native_data_021d720e[];
u32 native_main_020d3d74(void) {
    s16 sp0;
    u32 temp_r4;

    native_fn_02008be0(0, native_data_021d720e, 0x24);
    sp0 = 0;
    temp_r4 = native_fn_020d3b7c(&sp0, 1);
    return temp_r4 + native_fn_020d3b7c(&sp0, 0);
}
