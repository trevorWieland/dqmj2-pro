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
extern u32 native_fn_0200bd04(void *);
extern u32 native_fn_0200bfe4(void *, u32);
extern u32 native_fn_0200c170(void *, u32, u32);
extern u32 native_fn_0200c190(void *, u32, u32);
extern u32 native_data_020edec8;
extern u8 native_data_020edecc[];
u32 native_main_0202a954(u8 *arg0, u32 arg1, u32 arg2, u32 arg3, u32 arg4) {
    s32 var_r0;
    u32 var_r4 = 0;
    u32 var_r5;
    u8 *var_r8;

    var_r8 = arg0;
    if (var_r8 == NULL) {
        var_r8 = native_data_020edecc;
    }
    var_r5 = arg3;
    if (M2C_FIELD(var_r8, u8 *, 0) == 0) {
        if (M2C_FIELD(var_r8, u32 *, 0x18) & 1) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        if (var_r0 == 0) {
            native_fn_0200bd04(var_r8 + 0xC);
            if (native_fn_0200bfe4((void *) (var_r8 + 0xC), arg1) != 0) {
                if (var_r5 == 0) {
                    var_r5 = M2C_FIELD(var_r8, u32 *, 0x34) - M2C_FIELD(var_r8, u32 *, 0x30);
                }
                if (arg4 != 0) {
                    native_fn_0200c190((void *) (var_r8 + 0xC), arg4, 0U);
                }
                if (native_fn_0200c170((void *) (var_r8 + 0xC), arg2, var_r5) != 0) {
                    M2C_FIELD(var_r8, u32 *, 4) = var_r5;
                    M2C_FIELD(var_r8, u32 *, 8) = arg2;
                    var_r4 = 1;
                    M2C_FIELD(var_r8, u8 *, 0) = 1;
                    native_data_020edec8 = 0;
                } else {
                    native_data_020edec8 = 2;
                }
            } else {
                native_data_020edec8 = 1;
            }
        } else {
            native_data_020edec8 = 4;
        }
    } else {
        native_data_020edec8 = 5;
    }
    return var_r4;
}
