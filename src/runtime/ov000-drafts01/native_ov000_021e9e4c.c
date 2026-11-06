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
    u8 unknown_0[0x2];
    u8 field_2;
    u8 unknown_3[0x3];
    u8 field_6;
} Record_native_data_ov000_02236900;
extern Record_native_data_ov000_02236900 native_data_ov000_02236900;
u32 native_ov000_021e9e4c(u8 arg0, u8 arg1) {
    u16 temp_r2;

    temp_r2 = native_data_ov000_02236900.field_2 | (native_data_ov000_02236900.field_6 << 8);
    native_data_ov000_02236900.field_2 = arg0;
    native_data_ov000_02236900.field_6 = arg1;
    return (u32) temp_r2;
}
