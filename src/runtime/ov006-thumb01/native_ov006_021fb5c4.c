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
extern u32 native_fn_ov006_021fb358();
extern u32 native_fn_ov006_021fb4cc();
extern u8 native_data_ov006_0220b7fc[];
typedef struct {
    u8 field_0;
    u8 unknown_1[0x1];
    s8 field_2;
} Record_native_data_ov006_0221c0ec;
extern Record_native_data_ov006_0221c0ec native_data_ov006_0221c0ec;
u32 native_ov006_021fb5c4(u8 arg0) {
    native_data_ov006_0221c0ec.field_0 = arg0;
    native_data_ov006_0221c0ec.field_2 = (s8) native_fn_ov006_021fb358(native_data_ov006_0220b7fc[arg0]);
    return native_fn_ov006_021fb4cc();
}
