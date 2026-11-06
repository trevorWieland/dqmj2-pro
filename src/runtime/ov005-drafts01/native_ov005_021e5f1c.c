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
extern u32 native_fn_02008e0c();
typedef struct {
    u8 unknown_0[0x40];
    s32 field_40;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e5f1c(s32 arg0) {
    s32 temp_r3;
    s32 var_r4;
    s32 var_r5;

    var_r4 = 9;
    var_r5 = 0x36;
    do {
        temp_r3 = native_data_ov005_021ed438.field_40 + 2;
        native_fn_02008e0c(((var_r4 - 1) * 6) + temp_r3, temp_r3 + var_r5, 6);
        var_r4 -= 1;
        var_r5 -= 6;
    } while (var_r4 > 0);
    return native_fn_02008e0c(arg0, native_data_ov005_021ed438.field_40 + 2, 6);
}
