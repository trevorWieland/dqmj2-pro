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
extern u32 native_fn_0209bbe4();
extern u32 native_fn_020a3f70();
u32 native_main_020a4034(u32 arg0, u32 arg1, s32 arg2) {
    s32 sp0;
    s32 var_r5;
    u32 var_r6;
    u8 var_r4;

    var_r6 = arg0;
    sp0 = arg2;
    var_r4 = 0;
    do {
        if (var_r4 != 0) {
            var_r5 = 1 << var_r4;
        } else {
            var_r5 = 1;
        }
        if ((var_r6 & var_r5) && (var_r4 != native_fn_0209bbe4()) && (native_fn_020a3f70(var_r4, arg1, sp0) == 0)) {
            var_r6 &= ~var_r5;
        }
        var_r4 += 1;
    } while ((u32) var_r4 < 0x20U);
    return var_r6;
}
