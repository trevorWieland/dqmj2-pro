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
extern u32 native_fn_0209463c();
extern u32 native_fn_02094730();
extern u32 native_fn_0209477c();
extern u32 native_fn_02095194();
u32 native_main_020944c0(void) {
    u8 sp0;
    u8 temp_r0;

    sp0 = (u8) native_fn_0209477c();
    temp_r0 = sp0;
    if ((temp_r0 == 0) || (temp_r0 == 0x12)) {
        native_fn_0209463c();
        return 1U;
    }
    native_fn_02095194(&sp0);
    native_fn_02094730(sp0);
    return 0U;
}
