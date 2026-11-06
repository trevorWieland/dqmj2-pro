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
    u8 unknown_0[0x138];
    s8 field_138;
    s8 field_139;
    u8 unknown_13a[0x6];
    s32 field_140;
} Record_native_data_ov000_0223508c;
extern Record_native_data_ov000_0223508c native_data_ov000_0223508c;
typedef struct {
    u8 unknown_0[0x3c];
    s16 field_3c;
    s16 field_3e;
} Record_native_data_ov000_0223518c;
extern Record_native_data_ov000_0223518c native_data_ov000_0223518c;
u32 native_ov000_021e7160(s16 arg0, s8 arg1, s32 arg2) {
    native_data_ov000_0223508c.field_138 = 1;
    native_data_ov000_0223518c.field_3c = 0;
    native_data_ov000_0223518c.field_3e = arg0;
    native_data_ov000_0223508c.field_139 = arg1;
    native_data_ov000_0223508c.field_140 = arg2;
    return (u32) arg0;
}
