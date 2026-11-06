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
extern u32 native_fn_020946ec();
extern u32 native_fn_020947a8();
extern u32 native_fn_020952d0();
extern u32 native_fn_02095304();
extern u32 native_fn_0209530c();
extern u32 native_fn_02095324();
u32 native_main_0209529c(void) {
    s32 temp_r0;
    u32 temp_r4;

    temp_r4 = native_fn_020946ec(1);
    temp_r0 = (s32) native_fn_020947a8();
    if (temp_r0 < 4) {
        return native_fn_020952d0();
    }
    if (temp_r0 < 5) {
        return native_fn_02095304();
    }
    if (temp_r0 == 5) {
        return native_fn_0209530c(temp_r4);
    }
    return native_fn_02095324(temp_r4);
}
