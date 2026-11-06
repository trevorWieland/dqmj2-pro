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
extern u32 native_fn_02038d88();
extern u32 native_fn_0203917c();
extern u32 native_fn_0203928c();
extern u32 native_fn_020394f8();
u32 native_main_02039208(u32 arg0, s32 arg1, s32 arg2, s32 arg3, u32 *arg4) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r0_3;
    u32 var_r0;

    temp_r0_2 = native_fn_02038d88(arg0);
    if (temp_r0_2 == 0) {
        return 2U;
    }
    temp_r0 = native_fn_0203928c(M2C_FIELD(temp_r0_2, u16 *, 4), arg1, arg2, arg3, 0);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    temp_r0_3 = M2C_FIELD(temp_r0_2, u32 *, 0);
    if (arg1 & 1) {
        var_r0 = native_fn_020394f8(temp_r0_3, arg2, arg3);
        if (var_r0 == 0) {
            return 6U;
        }
        goto block_8;
    }
    var_r0 = native_fn_0203917c(temp_r0_3);
block_8:
    if (arg4 != NULL) {
        *arg4 = var_r0;
    }
    return 0U;
}
