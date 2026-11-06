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
extern u32 native_fn_0202b690();
extern u32 native_fn_0202b6dc();
u32 native_main_0202b7b8(u32 arg0, s32 arg1) {
    u32 temp_r5;
    u32 var_r0;

    var_r0 = arg0;
    temp_r5 = var_r0;
    if (arg1 & 1) {
        var_r0 = native_fn_0202b690();
    }
    if (!(arg1 & 2)) {
        return var_r0;
    }
    return native_fn_0202b6dc(temp_r5);
}
