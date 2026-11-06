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
extern u32 native_fn_02068fc0();
extern u32 native_fn_ov000_022162b4();
extern u32 native_fn_ov000_02217440();
u32 native_main_02078dd8(void) {
    u32 temp_r4;

    temp_r4 = native_fn_ov000_02217440();
    native_fn_02068fc0(0);
    native_fn_02068fc0(1);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0);
    native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 1);
    return native_fn_ov000_022162b4(M2C_FIELD(temp_r4, s8 *, 0x10), 0x7F);
}
