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
extern u32 native_fn_02008c58();
extern u32 native_fn_02048644();
extern u32 native_fn_02048a60();
extern u32 native_fn_02048a94();
extern u32 native_fn_02048a9c();
extern u32 native_fn_ov005_021da838();
typedef struct {
    u8 unknown_0[0x1c];
    s32 field_1c;
    s32 field_20;
    s32 field_24;
    s32 field_28;
    u8 unknown_2c[0x10];
    s32 field_3c;
    u8 unknown_40[0x14];
    s32 field_54;
    u8 unknown_58[0x14];
    s32 field_6c;
    s32 field_70;
    s32 field_74;
    s16 field_78;
} Record_native_data_ov005_021e9818;
extern Record_native_data_ov005_021e9818 native_data_ov005_021e9818;
extern u8 native_data_ov005_021e9ea8[];
extern u8 native_data_ov005_021ea5f8[];
u32 native_ov005_021decbc(void) {
    u32 temp_r0;
    s32 var_r9;
    u8 *var_r10;

    native_data_ov005_021e9818.field_20 = 0;
    native_data_ov005_021e9818.field_6c = 0x8000;
    native_data_ov005_021e9818.field_70 = 0xC000;
    native_data_ov005_021e9818.field_74 = 0;
    native_data_ov005_021e9818.field_78 = 0;
    native_data_ov005_021e9818.field_1c = 0x3C;
    native_data_ov005_021e9818.field_28 = 0x3C;
    native_data_ov005_021e9818.field_24 = 0;
    native_data_ov005_021e9818.field_3c = 0x5A;
    native_fn_02008c58(0, native_data_ov005_021e9ea8, 4);
    native_fn_ov005_021da838(native_data_ov005_021e9ea8);
    native_fn_02048a9c(native_data_ov005_021e9ea8, 3);
    native_fn_02048a94(native_data_ov005_021e9ea8, 0);
    M2C_FIELD(native_data_ov005_021e9ea8, s32 *, 0x7C) = (s32) (M2C_FIELD(native_data_ov005_021e9ea8, s32 *, 0x7C) | 2);
    native_fn_02048a60(native_data_ov005_021e9ea8, (s32) native_data_ov005_021e9818.field_6c >> 8, (s32) native_data_ov005_021e9818.field_70 >> 8);
    native_fn_02048644(native_data_ov005_021e9ea8, native_data_ov005_021e9818.field_54, 0x76);
    var_r9 = 0;
    var_r10 = native_data_ov005_021ea5f8;
    do {
        native_fn_02008c58(0, var_r10 + 0x14, 0x90);
        native_fn_ov005_021da838(var_r10 + 0x14);
        native_fn_02048a9c(var_r10 + 0x14, 3);
        native_fn_02048a94(var_r10 + 0x14, 0);
        native_fn_02048644(var_r10 + 0x14, native_data_ov005_021e9818.field_54, 0x6F);
        var_r9 += 1;
        temp_r0 = M2C_FIELD(var_r10, u32 *, 0x90) & ~2;
        M2C_FIELD(var_r10, u32 *, 0x90) = temp_r0;
        M2C_FIELD(var_r10, s8 *, 0x10) = 0;
        var_r10 += 0xA4;
    } while (var_r9 < 0xC);
    return temp_r0;
}
