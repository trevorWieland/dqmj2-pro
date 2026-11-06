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
extern u32 native_fn_0206dfd4();
extern u32 native_fn_0206e0c4();
extern u32 native_fn_0206e214();
u32 native_main_0206e100(void) {
    native_fn_0206dfd4();
    native_fn_0206e0c4();
    native_fn_0206e214();
    return native_fn_02045ed0(1);
}
