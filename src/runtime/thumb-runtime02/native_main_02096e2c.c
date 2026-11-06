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
extern u32 native_fn_02096ce8();
extern u32 native_fn_02096da4();
u32 native_main_02096e2c(u32 arg0, s32 arg1) {
    s32 var_r1;

    if (arg1 != 0) {
        var_r1 = 0x10 | native_fn_02096ce8();
    } else {
        var_r1 = native_fn_02096ce8() & ~0x10;
    }
    return native_fn_02096da4(arg0, var_r1);
}
