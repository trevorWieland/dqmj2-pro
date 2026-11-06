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
extern u32 native_fn_020094ec();
extern u32 native_fn_02009500();
u32 native_main_0200a288(s32 arg0, s32 arg1) {
    u32 var_r4;

    native_fn_020094ec();
    var_r4 = M2C_FIELD((arg0 + (arg1 * 4)), u32 *, 0x3C);
    if (var_r4 != 0) {
        if (var_r4 < 0x02000000U) {
            var_r4 = (u32)((u8 *)arg0 + var_r4);
        }
    } else {
        var_r4 = 0;
    }
    native_fn_02009500();
    return var_r4;
}
