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
extern u32 native_fn_0207b058();
extern u32 native_fn_0207d2c8();
extern u32 native_fn_0207d31c();
u32 native_main_0207d3d4(s32 arg0, u32 arg1, s32 arg2, s32 arg3, s32 *arg4, s32 arg5) {
    u8 temp_r0;
    u8 temp_r0_2;
    u8 temp_r0_3;
    u8 *temp_r4;
    u32 var_r8;

    var_r8 = arg1;
    temp_r4 = native_fn_0207d2c8();
    if (arg0 == 0) {
        return var_r8;
    }
    if ((arg2 == 1) && (arg3 == 0)) {
        if ((u32) (u8) (M2C_FIELD(temp_r4, u8 *, 1) + 0xF7) <= 1U) {
            var_r8 = native_fn_0207d31c(M2C_FIELD(temp_r4, u8 *, 2), var_r8, arg5);
        }
    }
    if (arg2 == 5) {
        temp_r0 = M2C_FIELD(temp_r4, u8 *, 1);
        if ((temp_r0 != 6) && (temp_r0 != 0xA)) {

        } else {
            var_r8 = native_fn_0207d31c(M2C_FIELD(temp_r4, u8 *, 2), var_r8, arg5);
        }
    }
    if ((arg2 == 4) && ((u32) (u8) (M2C_FIELD(temp_r4, u8 *, 1) + 0xF9) <= 1U)) {
        var_r8 = native_fn_0207d31c(M2C_FIELD(temp_r4, u8 *, 2), var_r8, arg5);
    }
    if (arg2 == 3) {
        temp_r0_2 = M2C_FIELD(temp_r4, u8 *, 1);
        if ((temp_r0_2 != 3) && (temp_r0_2 != 8)) {

        } else {
            var_r8 = native_fn_0207d31c(M2C_FIELD(temp_r4, u8 *, 2), var_r8, arg5);
        }
    }
    if ((arg2 == 6) && (M2C_FIELD(temp_r4, u8 *, 1) == 2)) {
        var_r8 = native_fn_0207d31c(M2C_FIELD(temp_r4, u8 *, 2), var_r8, arg5);
    }
    if ((arg2 == 7) && (M2C_FIELD(temp_r4, u8 *, 1) == 4)) {
        var_r8 = native_fn_0207d31c(M2C_FIELD(temp_r4, u8 *, 2), var_r8, arg5);
    }
    if ((arg2 == 2) && (M2C_FIELD(temp_r4, u8 *, 1) == 5)) {
        var_r8 = native_fn_0207d31c(M2C_FIELD(temp_r4, u8 *, 2), var_r8, arg5);
    }
    if ((arg4 != NULL) && (M2C_FIELD(temp_r4, u8 *, 1) == 1) && (native_fn_0207b058(arg5, 4) != 0)) {
        temp_r0_3 = M2C_FIELD(temp_r4, u8 *, 2);
        switch (temp_r0_3) {
        case 4:
            *arg4 += 3;
            break;
        case 2:
            *arg4 += 1;
            break;
        case 3:
            *arg4 += 2;
            break;
        }
    }
    return var_r8;
}
