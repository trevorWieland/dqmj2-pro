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
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    u8 unknown_2[0x1];
    s8 field_3;
    s8 field_4;
    u8 unknown_5[0x1];
    s16 field_6;
} Record_native_data_ov006_0220f594;
extern Record_native_data_ov006_0220f594 native_data_ov006_0220f594;
u32 native_ov006_021de964(s8 arg0, s8 arg1, s16 arg2, s8 arg3) {
    native_data_ov006_0220f594.field_3 = arg3;
    native_data_ov006_0220f594.field_1 = arg0;
    native_data_ov006_0220f594.field_4 = arg1;
    native_data_ov006_0220f594.field_6 = arg2;
    return (u32) arg0;
}
