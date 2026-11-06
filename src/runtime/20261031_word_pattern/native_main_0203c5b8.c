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
extern u32 native_fn_02008c58(u32 value, s32 *destination, u32 bytes);
extern u8 native_data_020f5bf0[];
extern u8 native_data_020f5c00[];
u32 native_main_0203c5b8(u8 *arg0) {
    s32 temp_r2;
    u8 *var_r4;

    var_r4 = arg0;
    if (var_r4 == NULL) {
        var_r4 = native_data_020f5c00;
    }
    temp_r2 = M2C_FIELD(var_r4, s32 *, 4);
    if (temp_r2 > 0) {
        if (M2C_FIELD(var_r4, u8 *, 8) == 0) {
            native_fn_02008c58(1, M2C_FIELD(var_r4, s32 **, 0), (temp_r2 - 1) * 4);
            M2C_FIELD(&M2C_FIELD(var_r4, s32 **, 0)[M2C_FIELD(var_r4, s32 *, 4)], s32 *, -4) = 0;
        } else {
            native_fn_02008c58(2, M2C_FIELD(var_r4, s32 **, 0) + 1, (temp_r2 - 1) * 4);
            *M2C_FIELD(var_r4, s32 **, 0) = 0;
        }
        *native_data_020f5bf0 = 0;
        return 1U;
    }
    *native_data_020f5bf0 = 1;
    return 0U;
}
