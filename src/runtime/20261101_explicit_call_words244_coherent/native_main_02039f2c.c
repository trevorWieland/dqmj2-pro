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
#define NULL ((void *)0)
extern u32 native_fn_02038f18(u32);
extern u32 native_fn_0203a28c(u32, u32, u32, u32, u32, u32, u32, u32, u32, u32);
u32 native_main_02039f2c(u32 arg0, s32 arg1, s32 arg2, u32 arg3, s32 arg4) {
    u32 temp_r0;
    s32 var_r5;
    s32 var_r6;

    var_r6 = arg1;
    var_r5 = arg2;
    temp_r0 = native_fn_02038f18(arg3);
    if (temp_r0 == 0) {
        return 0U;
    }
    if (var_r5 < 0) {
        var_r5 = (s32) M2C_FIELD(temp_r0, u8 *, 5);
    }
    if (var_r6 < 0) {
        var_r6 = (s32) M2C_FIELD(temp_r0, u8 *, 6);
    }
    return native_fn_0203a28c(arg0, temp_r0, var_r6, var_r5, arg3, arg4, 0, 0, 0, 0);
}
