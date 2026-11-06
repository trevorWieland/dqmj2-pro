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
extern u32 native_fn_02041800();
extern u32 native_fn_02041814();
typedef struct {
    u8 unknown_0[0x38];
    u32 field_38;
    u8 unknown_3c[0x20];
    u32 field_5c;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e4e48(void) {
    u32 var_r4;

    var_r4 = native_data_ov005_021ed438.field_5c;
    if (native_fn_02041814() == 1) {
        return var_r4;
    }
    if (native_fn_02041800() != 1) {
        var_r4 = native_data_ov005_021ed438.field_38;
    }
    return var_r4;
}
