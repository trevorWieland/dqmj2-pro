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
    u8 unknown_0[0x17];
    s8 field_17;
    u8 unknown_18[0x2];
    s8 field_1a;
    u8 unknown_1b[0xe];
    s8 field_29;
    u8 unknown_2a[0xe];
    s16 field_38;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
u32 native_ov001_021e97a4(s8 arg0, s8 arg1, s16 arg2, s8 arg3) {
    native_data_ov001_02238d7c.field_1a = arg0;
    native_data_ov001_02238d7c.field_17 = arg1;
    native_data_ov001_02238d7c.field_38 = arg2;
    native_data_ov001_02238d7c.field_29 = arg3;
    return (u32) arg0;
}
