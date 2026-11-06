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
extern u32 native_fn_020a8594();
extern u32 native_fn_020a929c();
u32 native_main_020a8614(void *arg0) {
    s32 var_r4;

    var_r4 = 0;
    if ((s32) M2C_FIELD(arg0, s32 *, 0) > 0) {
        do {
            native_fn_020a8594(arg0, var_r4);
            var_r4 += 1;
        } while (var_r4 < (s32) M2C_FIELD(arg0, s32 *, 0));
    }
    native_fn_020a929c(M2C_FIELD(arg0, void **, 0x14));
    return native_fn_020a929c(arg0);
}
