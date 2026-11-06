#define NULL ((void *)0)
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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_020a8ec4();
extern u32 native_fn_020b0e04();
extern u32 native_fn_020b0e78();
extern u32 native_fn_020b2a38();
extern u32 native_fn_020b2c88();
extern u8 native_data_020e1234[];
u32 native_main_020b0ecc(s32 arg0, s8 *arg1, s8 *arg2, s8 *arg3, s8 *arg4, s8 *arg5, s32 arg6, s32 arg7, s32 arg8, s32 arg9, s32 argA) {
    u32 var_r0;
    void *spC;
    s8 *sp8;
    s32 sp4;

    sp4 = arg0;
    sp8 = arg3;
    if (((arg1 == NULL) || (*arg1 == 0)) && ((sp8 == NULL) || (*sp8 == 0)) && ((arg4 == NULL) || (*arg4 == 0)) && ((arg5 == NULL) || (*arg5 == 0)) && (arg6 == 0) && ((arg2 == NULL) || (*arg2 == 0))) {
        native_fn_020b2c88(sp4, native_data_020e1234);
        return 2U;
    }
    var_r0 = native_fn_020b0e04(sp4, &spC, 1);
    if (var_r0 == 0) {
        if (arg1 == NULL) {
            M2C_FIELD(spC, s8 *, 0x28) = 0;
        } else {
            native_fn_020b2a38(spC + 0x28, arg1, 0x1F);
        }
        if (arg2 == NULL) {
            M2C_FIELD(spC, s8 *, 0x47) = 0;
        } else {
            native_fn_020b2a38(spC + 0x47, arg2, 0x15);
        }
        if (sp8 == NULL) {
            M2C_FIELD(spC, s8 *, 0x5C) = 0;
        } else {
            native_fn_020b2a38(spC + 0x5C, sp8, 0x33);
        }
        native_fn_020a8ec4(spC + 0x5C);
        if (arg4 == NULL) {
            M2C_FIELD(spC, s8 *, 0x8F) = 0;
        } else {
            native_fn_020b2a38(spC + 0x8F, arg4, 0x1F);
        }
        if (arg5 == NULL) {
            M2C_FIELD(spC, s8 *, 0xAE) = 0;
        } else {
            native_fn_020b2a38(spC + 0xAE, arg5, 0x1F);
        }
        M2C_FIELD(spC, s32 *, 0x134) = arg6;
        if (arg7 < 0) {
            arg7 = 0;
        }
        M2C_FIELD(spC, s32 *, 0x138) = arg7;
        var_r0 = native_fn_020b0e78(sp4, spC, arg8, arg9, argA);
        if (var_r0 == 0) {
            var_r0 = 0;
        }
    }
    return var_r0;
}
