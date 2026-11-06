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
    u8 unknown_0[0x3];
    s8 field_3;
    s8 field_4;
    s8 field_5;
    u8 unknown_6[0x8];
    s16 field_e;
} Record_native_data_ov001_02242b50;
extern Record_native_data_ov001_02242b50 native_data_ov001_02242b50;
u32 native_ov001_022148a0(s8 arg0, s8 arg1, s16 arg2, s8 arg3) {
    native_data_ov001_02242b50.field_3 = arg0;
    native_data_ov001_02242b50.field_4 = arg1;
    native_data_ov001_02242b50.field_e = arg2;
    native_data_ov001_02242b50.field_5 = arg3;
    return (u32) arg0;
}
