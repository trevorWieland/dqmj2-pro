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
extern u32 native_fn_020b0e04();
extern u32 native_fn_020b0e78();
u32 native_main_020b1004(u32 arg0, s32 arg1, s32 arg2, u32 arg3, s32 arg4, s32 arg5) {
    void *sp4;
    u32 var_r0;

    var_r0 = native_fn_020b0e04(arg0, &sp4, 9);
    if (var_r0 == 0) {
        M2C_FIELD(sp4, s32 *, 0x14C) = arg1;
        M2C_FIELD(sp4, s32 *, 0x150) = arg2;
        var_r0 = native_fn_020b0e78(arg0, sp4, arg3, arg4, arg5);
        if (var_r0 == 0) {
            var_r0 = 0;
        }
    }
    return var_r0;
}
