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
extern u32 native_fn_ov005_021d9060();
extern u32 native_fn_ov005_021d90f0();
typedef struct {
    u8 unknown_0[0x2c];
    s32 field_2c;
    s32 field_30;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e6360(void) {
    if (native_data_ov005_021ed438.field_2c == 0) {
        return 1U;
    }
    if ((native_data_ov005_021ed438.field_30 == 1) && (native_fn_ov005_021d90f0() == 0)) {
        native_data_ov005_021ed438.field_2c = 0;
        return 1U;
    }
    if ((native_data_ov005_021ed438.field_2c == 1) && (native_data_ov005_021ed438.field_30 == 0)) {
        native_data_ov005_021ed438.field_30 = 1;
        native_fn_ov005_021d9060();
    }
    return 0U;
}
