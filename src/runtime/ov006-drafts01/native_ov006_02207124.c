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
extern u32 native_fn_02049e0c();
extern u32 native_fn_0204b380();
extern u32 native_fn_0204b61c();
extern u32 native_fn_ov006_021e648c();
extern u32 native_fn_ov006_021e7e90();
extern u8 native_data_ov006_0220bc0c[];
typedef struct {
    u8 unknown_0[0x8];
    s32 field_8;
} Record_native_data_ov006_0221c27c;
extern Record_native_data_ov006_0221c27c native_data_ov006_0221c27c;
extern u8 native_data_ov006_0221c2c0[];
extern u8 native_data_ov006_0221c350[];
u32 native_ov006_02207124(s32 arg0) {
    if (arg0 != 0) {
        native_fn_ov006_021e7e90(native_data_ov006_0220bc0c);
        native_fn_02049e0c(0);
        native_data_ov006_0221c27c.field_8 = 5;
    }
    native_fn_0204b61c(native_data_ov006_0221c350, 0);
    native_fn_0204b380(native_data_ov006_0221c2c0, 0);
    return native_fn_ov006_021e648c(arg0);
}
