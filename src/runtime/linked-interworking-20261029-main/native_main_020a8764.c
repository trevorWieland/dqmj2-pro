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
extern u32 native_fn_02026144();
extern u32 native_fn_020a8644();
extern u32 native_fn_020a8844();
extern u32 native_fn_020a8884();
u32 native_main_020a8764(void *arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    u32 var_r0;
    s32 temp_r6;
    s32 spC;
    s32 sp8;

    sp8 = arg1;
    spC = 1;
    if ((arg0 == NULL) || (temp_r6 = M2C_FIELD(arg0, s32 *, 0), (temp_r6 == 0))) {
        return -1U;
    }
    if (arg4 != 0) {
        var_r0 = native_fn_020a8884(sp8, native_fn_020a8644(arg0, arg3), temp_r6 - arg3, M2C_FIELD(arg0, s32 *, 8), arg2, &spC);
    } else {
        var_r0 = native_fn_020a8844(sp8, native_fn_020a8644(arg0, arg3), temp_r6 - arg3, M2C_FIELD(arg0, s32 *, 8), arg2);
    }
    if ((var_r0 != 0) && (spC != 0)) {
        return native_fn_02026144(var_r0 - M2C_FIELD(arg0, s32 *, 0x14), M2C_FIELD(arg0, s32 *, 8));
    }
    return -1U;
}
