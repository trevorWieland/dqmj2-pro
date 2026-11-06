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
extern u32 native_fn_020a6e34();
extern u32 native_fn_020a6ea8();
extern u32 native_fn_020a8640();
extern u32 native_fn_020a8644();
extern u32 native_fn_020a8828();
u32 native_main_020a6ee0(void *arg0) {
    s32 temp_r0;
    s32 var_r4;

    temp_r0 = (s32) native_fn_020a8640(M2C_FIELD(arg0, s32 *, 4));
    var_r4 = 0;
    if (temp_r0 > 0) {
        do {
            native_fn_020a6e34(arg0, *(s32 *) native_fn_020a8644(M2C_FIELD(arg0, s32 *, 4), var_r4));
            var_r4 += 1;
        } while (var_r4 < temp_r0);
    }
    native_fn_020a8828(M2C_FIELD(arg0, s32 *, 4));
    return native_fn_020a6ea8(arg0);
}
