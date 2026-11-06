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
extern u32 native_fn_02045dc4();
extern u32 native_fn_0204861c();
extern u32 native_fn_0205f920();
extern u32 native_fn_ov006_021e7608();
extern u8 native_data_ov006_02218e18[];
extern u8 native_data_ov006_02218e60[];
typedef struct {
    u8 unknown_0[0x7c];
    s32 field_7c;
    u8 unknown_80[0x1];
    u8 field_81;
} Record_native_data_ov006_02218ea8;
extern Record_native_data_ov006_02218ea8 native_data_ov006_02218ea8;
typedef struct {
    u8 unknown_0[0x7c];
    s32 field_7c;
    u8 unknown_80[0x1];
    u8 field_81;
} Record_native_data_ov006_02218f38;
extern Record_native_data_ov006_02218f38 native_data_ov006_02218f38;
u32 native_ov006_021e9008(void) {
    s32 var_r4;

    native_fn_02045dc4(1, 3, 1, 3, 0x1E, 0x14);
    var_r4 = 0;
    do {
        native_fn_ov006_021e7608(var_r4);
        var_r4 += 1;
    } while (var_r4 < 0xD);
    native_fn_0205f920(native_data_ov006_02218e18, 1, 2);
    native_fn_0205f920(native_data_ov006_02218e60, 1, 2);
    native_data_ov006_02218f38.field_7c = (s32) (native_data_ov006_02218f38.field_7c & ~2);
    native_data_ov006_02218ea8.field_7c = (s32) (native_data_ov006_02218ea8.field_7c & ~2);
    native_fn_0204861c(1, native_data_ov006_02218f38.field_81);
    return native_fn_0204861c(1, native_data_ov006_02218ea8.field_81);
}
