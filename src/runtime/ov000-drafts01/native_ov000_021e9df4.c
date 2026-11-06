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
extern u32 native_fn_02002c98();
extern u32 native_fn_02003ba0();
extern u32 native_fn_02008070();
extern u32 native_fn_ov000_021e8ec8();
typedef struct {
    u8 unknown_0[0x7];
    u8 field_7;
} Record_native_data_ov000_02236900;
extern Record_native_data_ov000_02236900 native_data_ov000_02236900;
u32 native_ov000_021e9df4(u8 arg0) {
    u8 temp_r4;

    temp_r4 = native_data_ov000_02236900.field_7;
    if (arg0 != 0) {
        native_fn_02003ba0();
        native_fn_ov000_021e8ec8();
        native_fn_02008070();
        native_fn_02002c98(0xA, 4, 1);
    } else {
        native_fn_02002c98(1, 0, 1);
    }
    native_data_ov000_02236900.field_7 = arg0;
    return (u32) temp_r4;
}
