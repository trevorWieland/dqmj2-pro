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
extern u32 native_fn_020a6f78();
extern u32 native_fn_020a8614();
extern u32 native_fn_020a8640();
extern u32 native_fn_020a8644();
u32 native_main_020a75ec(void *arg0) {
    s32 var_r4;
    u32 var_r0;

    var_r0 = M2C_FIELD(arg0, u32 *, 8);
    if (var_r0 != 0) {
        var_r4 = 0;
        if ((s32) native_fn_020a8640() > 0) {
            do {
                native_fn_020a6f78(arg0, *(s32 *) native_fn_020a8644(M2C_FIELD(arg0, u32 *, 8), var_r4));
                var_r4 += 1;
            } while (var_r4 < (s32) native_fn_020a8640(M2C_FIELD(arg0, u32 *, 8)));
        }
        native_fn_020a8614(M2C_FIELD(arg0, u32 *, 8));
        var_r0 = 0;
        M2C_FIELD(arg0, u32 *, 8) = 0U;
    }
    return var_r0;
}
