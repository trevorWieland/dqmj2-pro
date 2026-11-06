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
extern u32 native_fn_020aae0c();
extern u32 native_fn_020afa1c();
extern u32 native_fn_020b0cd4();
u32 native_main_020b0e78(void **arg0, u32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    void *spC;
    u32 var_r0;
    void *temp_r1;

    temp_r1 = *arg0;
    M2C_FIELD(temp_r1, s32 *, 0x238) = (s32) (M2C_FIELD(temp_r1, s32 *, 0x238) + 1);
    var_r0 = native_fn_020afa1c(arg0, 3, arg1, &spC, arg2, arg3, arg4);
    if (var_r0 == 0) {
        var_r0 = native_fn_020b0cd4(arg0, spC);
        if ((var_r0 == 0) && ((M2C_FIELD(spC, s32 *, 8) == 0) || (var_r0 = native_fn_020aae0c(arg0, M2C_FIELD(spC, s32 *, 0x18)), (var_r0 == 0)))) {
            var_r0 = 0;
        }
    }
    return var_r0;
}
