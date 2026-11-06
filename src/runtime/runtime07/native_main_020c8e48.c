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
extern u32 native_fn_0202a1e0();
extern u32 native_fn_02045680();
extern u32 native_fn_02046150();
extern u32 native_fn_02048f1c();
extern u32 native_fn_02048f2c();
extern u32 native_fn_02048f3c();
extern u32 native_fn_02048f4c();
extern u32 native_fn_020c3e9c();
extern u32 native_fn_020c3f94();
extern u32 native_fn_020c5f74();
extern u32 native_fn_020c70cc();
u32 native_main_020c8e48(void) {
    u32 temp_r4;

    native_fn_020c3e9c();
    native_fn_02048f1c(1, 1);
    native_fn_02048f2c(0, 1);
    native_fn_02048f3c(2, 1);
    native_fn_02048f4c(3, 1);
    native_fn_02045680(0);
    native_fn_02045680(1);
    native_fn_02045680(2);
    native_fn_02045680(3);
    native_fn_02046150(1, 0, 2);
    native_fn_02046150(2, 2, 2);
    temp_r4 = native_fn_0202a1e0(2U);
    native_fn_020c3f94();
    native_fn_020c5f74();
    native_fn_020c70cc();
    return native_fn_0202a1e0(temp_r4);
}
