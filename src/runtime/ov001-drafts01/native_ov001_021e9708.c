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
extern u32 native_fn_02008d78();
extern u32 native_fn_ov001_021e1348();
extern u32 native_fn_ov001_0221429c();
extern u32 native_fn_ov001_022142c0();
extern u8 native_data_ov001_0222ec84[];
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    u8 unknown_3[0x8];
    s8 field_b;
    u8 unknown_c[0x7];
    s8 field_13;
    s8 field_14;
    u8 unknown_15[0x1];
    s8 field_16;
    u8 unknown_17[0x2];
    s8 field_19;
    u8 unknown_1a[0x3];
    s8 field_1d;
    s8 field_1e;
    s8 field_1f;
    u8 unknown_20[0x4];
    s8 field_24;
    u8 unknown_25[0x2];
    s8 field_27;
    u8 unknown_28[0x28];
    u32 field_50;
    u32 field_54;
    u8 unknown_58[0x8];
    u32 field_60;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
extern u8 native_data_ov001_02238de0[];
u32 native_ov001_021e9708(s8 arg0) {
    native_data_ov001_02238d7c.field_60 = native_fn_ov001_0221429c();
    native_data_ov001_02238d7c.field_54 = native_fn_ov001_022142c0();
    native_data_ov001_02238d7c.field_24 = (s8) native_fn_ov001_021e1348();
    native_data_ov001_02238d7c.field_19 = 0;
    native_data_ov001_02238d7c.field_1f = 0;
    native_data_ov001_02238d7c.field_14 = 1;
    native_data_ov001_02238d7c.field_50 = native_fn_ov001_0221429c();
    native_data_ov001_02238d7c.field_27 = -1;
    native_fn_02008d78(native_data_ov001_02238de0, 0, 0xC);
    native_data_ov001_02238d7c.field_b = 0;
    M2C_FIELD(native_data_ov001_0222ec84, s8 *, 1) = 0;
    native_data_ov001_02238d7c.field_16 = 0;
    native_data_ov001_02238d7c.field_1d = 0;
    native_data_ov001_02238d7c.field_2 = arg0;
    native_data_ov001_02238d7c.field_1e = 0;
    native_data_ov001_02238d7c.field_13 = 0;
    return (u32) native_data_ov001_0222ec84;
}
