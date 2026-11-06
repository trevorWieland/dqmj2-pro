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
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
extern void native_fn_02008064(u32);
extern u32 native_fn_02009dbc(void);
extern u8 native_data_020e3780[];
extern u32 *native_data_020e37a4[];
u32 native_main_020095e8(u32 arg0) {
    s32 temp_r1;
    u32 *var_r2;
    u32 var_r4;
    u32 *temp_r5;

    var_r4 = native_fn_02007ff4();
    if (arg0 & 1) {
        if (M2C_FIELD(native_data_020e3780, s32 *, 4) == native_fn_02009dbc()) {
            do {
                native_fn_02008008(var_r4);
                native_fn_02008064(0x64U);
                var_r4 = native_fn_02007ff4();
            } while (M2C_FIELD(native_data_020e3780, s32 *, 4) == native_fn_02009dbc());
        }
        goto block_7;
    }
    if (M2C_FIELD(native_data_020e3780, s32 *, 4) == native_fn_02009dbc()) {
        native_fn_02008008(var_r4);
        return 0U;
    }
block_7:
    temp_r5 = native_data_020e37a4[M2C_FIELD(native_data_020e3780, s32 *, 0x14)];
    temp_r1 = M2C_FIELD(native_data_020e3780, s32 *, 0x14) + 1;
    M2C_FIELD(native_data_020e3780, s32 *, 0x14) = temp_r1;
    if (temp_r1 > 8) {
        M2C_FIELD(native_data_020e3780, s32 *, 0x14) = 0;
    }
    var_r2 = temp_r5;
    if (*temp_r5 != 0) {
        do {
            var_r2 = *var_r2;
        } while (*var_r2 != 0);
    }
    if (M2C_FIELD(native_data_020e3780, u32 **, 0x10) != NULL) {
        *M2C_FIELD(native_data_020e3780, u32 **, 0x10) = temp_r5;
    } else {
        M2C_FIELD(native_data_020e3780, u32 **, 0) = temp_r5;
    }
    M2C_FIELD(native_data_020e3780, u32 **, 0x10) = var_r2;
    M2C_FIELD(native_data_020e3780, s32 *, 0x1C) = (s32) (M2C_FIELD(native_data_020e3780, s32 *, 0x1C) - 1);
    M2C_FIELD(native_data_020e3780, s32 *, 4) = (s32) (M2C_FIELD(native_data_020e3780, s32 *, 4) + 1);
    native_fn_02008008(var_r4);
    return (u32) temp_r5;
}
