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
extern u32 native_fn_0207d0c8(u32 arg0, u32 arg1);
extern u32 native_fn_0207d0f8(u32 arg0, u32 arg1, s32 arg2);
extern u32 native_fn_0207d144(u32 arg0, const u8 *arg1);
u32 native_main_0207ce3c(const u8 *arg0, u32 arg1, u32 arg2) {
    s32 temp_r2;
    s32 var_r8;
    u32 var_r2;
    u8 temp_r0;
    u8 temp_r0_2;

    var_r2 = arg2;
    if (var_r2 == 0) {
        return 0U;
    }
    var_r8 = 0;
    while ((var_r8 < 0x40) && ((temp_r0 = arg0[var_r8]) != 0)) {
        if (temp_r0 == 0x10) {
            var_r2 = native_fn_0207d0c8(arg1, var_r2);
        }
        if (*(arg0 + var_r8) == 0x11) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 1U);
        }
        if (*(arg0 + var_r8) == 0x12) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 2U);
        }
        if (*(arg0 + var_r8) == 0x13) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 3U);
        }
        if (*(arg0 + var_r8) == 0x14) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 4U);
        }
        if (*(arg0 + var_r8) == 0x15) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 5U);
        }
        if (*(arg0 + var_r8) == 0x16) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 6U);
        }
        if (*(arg0 + var_r8) == 0x46) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 0x18U);
        }
        if (*(arg0 + var_r8) == 0xFA) {
            var_r2 = native_fn_0207d0f8(arg1, var_r2, 0x1CU);
        }
        temp_r0_2 = *(arg0 + var_r8);
        if (temp_r0_2 == 0x19) {
            temp_r2 = var_r2 * 3;
            var_r2 = (u32) ((s32) (temp_r2 + ((u32) (temp_r2 >> 1) >> 0x1E)) >> 2);
            if ((s32) var_r2 < 1) {
                var_r2 = 1;
            }
        }
        if (temp_r0_2 == 0x1A) {
            var_r2 = (u32) ((s32) (var_r2 + (var_r2 >> 0x1F)) >> 1);
            if ((s32) var_r2 < 1) {
                var_r2 = 1;
            }
        }
        if (temp_r0_2 == 0x3C) {
            var_r2 *= 2;
        }
        var_r8 += 1;
    }
    return native_fn_0207d144(var_r2, arg0);
}
