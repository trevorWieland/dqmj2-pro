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
extern u32 native_fn_02063144();
extern u32 native_fn_ov001_02213a08();
extern u32 native_fn_ov001_02213a28();
extern u32 native_fn_ov001_02213a4c();
typedef struct {
    u8 unknown_0[0x2];
    u8 field_2;
} Record_native_data_ov001_02242998;
extern Record_native_data_ov001_02242998 native_data_ov001_02242998;
extern u8 native_data_ov001_022429ac[];
u32 native_ov001_02213adc(void) {
    u8 var_r4;

    native_fn_02008c58(0, native_data_ov001_022429ac, 0x100);
    var_r4 = 0;
    native_data_ov001_02242998.field_2 = 0U;
    do {
        if ((native_fn_ov001_02213a08(var_r4) != 0) && (native_fn_02063144(var_r4) != 0)) {
            native_fn_ov001_02213a28(var_r4);
        }
        var_r4 += 1;
    } while ((u32) var_r4 < 0xFFU);
    native_fn_ov001_02213a4c();
    return (u32) native_data_ov001_02242998.field_2;
}
