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
extern u32 native_fn_ov006_021edbac();
typedef struct {
    u8 unknown_0[0x10];
    s32 field_10;
    u8 unknown_14[0x10];
    s32 field_24;
    s32 field_28;
    s32 field_2c;
    s32 field_30;
    s32 field_34;
} Record_native_data_ov006_02219b4c;
extern Record_native_data_ov006_02219b4c native_data_ov006_02219b4c;
extern u8 native_data_ov006_02219b6c[];
extern u8 native_data_ov006_02219b70[];
extern u8 native_data_ov006_0221a8ac[];
u32 native_ov006_021ec688(void *arg0) {
    native_fn_ov006_021edbac(native_data_ov006_0221a8ac, 0, 8);
    native_data_ov006_02219b4c.field_10 = 1;
    native_fn_ov006_021edbac(native_data_ov006_02219b70, 0, 0x1C);
    native_data_ov006_02219b4c.field_24 = (s32) (arg0 + 6);
    native_data_ov006_02219b4c.field_28 = (s32) M2C_FIELD(arg0, u16 *, 4);
    native_data_ov006_02219b4c.field_2c = (s32) (0xF & M2C_FIELD(arg0, u16 *, 0));
    M2C_FIELD(native_data_ov006_02219b6c, u8 *, 0x1D) = (u8) M2C_FIELD(arg0, u8 *, 2);
    native_data_ov006_02219b4c.field_30 = 0;
    native_data_ov006_02219b4c.field_34 = 0xC0A80B01;
    M2C_FIELD(native_data_ov006_02219b6c, s8 *, 0x1C) = 0;
    return (u32) native_data_ov006_02219b6c;
}
