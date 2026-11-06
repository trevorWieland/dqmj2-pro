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
    u8 unknown_2a[0xc];
    u16 field_36;
    u16 field_38;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
u32 native_ov001_021e95d8(u16 arg0) {
    u16 temp_lr;

    temp_lr = native_data_ov001_02238d7c.field_36;
    native_data_ov001_02238d7c.field_36 = arg0;
    native_data_ov001_02238d7c.field_1a = 7;
    native_data_ov001_02238d7c.field_17 = 0;
    native_data_ov001_02238d7c.field_38 = arg0;
    native_data_ov001_02238d7c.field_29 = -1;
    return (u32) temp_lr;
}
