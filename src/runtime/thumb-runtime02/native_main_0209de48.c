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
extern u32 native_fn_0209a9e4();
extern u32 native_fn_020a3d70();
extern u32 native_fn_020a601c();
extern u32 native_fn_020a699c();
u32 native_main_0209de48(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 var_r4;

    var_r4 = arg2;
    if ((native_fn_020a3d70() == 0) || (native_fn_0209a9e4() != 0)) {
        return var_r4;
    }
    temp_r0 = native_fn_020a699c(M2C_FIELD((void *) native_fn_020a3d70(), s32 *, 0xE4), arg0);
    if (temp_r0 != 0) {
        var_r4 = native_fn_020a601c(temp_r0, arg1, var_r4);
    }
    return var_r4;
}
