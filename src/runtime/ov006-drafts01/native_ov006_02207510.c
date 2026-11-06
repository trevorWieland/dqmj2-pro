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
extern u32 native_fn_0204861c();
extern u32 native_fn_0205f920();
extern u32 native_fn_0207cdb8();
extern u32 native_fn_ov006_021e6494();
extern u32 native_fn_ov006_021e7210();
extern u32 native_fn_ov006_021e7268();
extern u32 native_fn_ov006_021e7608();
extern u32 native_fn_ov006_021e7d78();
extern u32 native_fn_ov006_021eacf8();
extern u32 native_fn_ov006_02206374();
extern u8 native_data_ov006_0220e96c[];
extern u8 native_data_ov006_0221c2c0[];
extern u8 native_data_ov006_0221c308[];
extern u8 native_data_ov006_0221c350[];
typedef struct {
    u8 unknown_0[0x81];
    u8 field_81;
} Record_native_data_ov006_0221c49c;
extern Record_native_data_ov006_0221c49c native_data_ov006_0221c49c;
typedef struct {
    u8 unknown_0[0x81];
    u8 field_81;
} Record_native_data_ov006_0221c52c;
extern Record_native_data_ov006_0221c52c native_data_ov006_0221c52c;
typedef struct {
    u8 unknown_0[0x81];
    u8 field_81;
} Record_native_data_ov006_0221c5bc;
extern Record_native_data_ov006_0221c5bc native_data_ov006_0221c5bc;
typedef struct {
    u8 unknown_0[0x81];
    u8 field_81;
} Record_native_data_ov006_0221c64c;
extern Record_native_data_ov006_0221c64c native_data_ov006_0221c64c;
u32 native_ov006_02207510(void) {
    s32 var_r4;

    native_fn_ov006_021eacf8(0);
    native_fn_ov006_021e7d78();
    var_r4 = 0;
    do {
        native_fn_ov006_021e7608(var_r4);
        var_r4 += 1;
    } while (var_r4 < 3);
    native_fn_0205f920(native_data_ov006_0221c2c0, 1, 2);
    native_fn_0205f920(native_data_ov006_0221c350, 1, 2);
    native_fn_0205f920(native_data_ov006_0221c308, 1, 2);
    native_fn_0204861c(1, native_data_ov006_0221c52c.field_81);
    native_fn_0204861c(1, native_data_ov006_0221c64c.field_81);
    native_fn_0204861c(1, native_data_ov006_0221c49c.field_81);
    native_fn_0204861c(1, native_data_ov006_0221c5bc.field_81);
    native_fn_ov006_02206374();
    native_fn_ov006_021e7268();
    native_fn_ov006_021e7210(native_data_ov006_0220e96c, 4);
    native_fn_0207cdb8(1);
    return native_fn_ov006_021e6494();
}
