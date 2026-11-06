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
extern u32 native_fn_ov001_021e1328();
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    u8 unknown_3[0x4];
    s8 field_7;
    u8 unknown_8[0x8];
    u32 field_10;
} Record_native_data_ov001_02242b50;
extern Record_native_data_ov001_02242b50 native_data_ov001_02242b50;
u32 native_ov001_02214308(s8 arg0) {
    u32 temp_r0;

    temp_r0 = native_fn_ov001_021e1328();
    native_data_ov001_02242b50.field_10 = temp_r0;
    native_data_ov001_02242b50.field_7 = arg0;
    native_data_ov001_02242b50.field_2 = 0;
    return temp_r0;
}
