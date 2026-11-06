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
extern u32 native_fn_ov006_021fe5ac();
extern u32 native_fn_ov006_0220490c();
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    s32 field_8;
} Record_native_data_ov006_0221c134;
extern Record_native_data_ov006_0221c134 native_data_ov006_0221c134;
u32 native_ov006_021fe580(s32 arg0, s32 arg1, s32 arg2) {
    native_data_ov006_0221c134.field_4 = (s32) (arg0 + (arg1 << 5));
    native_data_ov006_0221c134.field_8 = (s32) ((arg2 << 5) + 0x05000000);
    return native_fn_ov006_0220490c(1, native_fn_ov006_021fe5ac, 0, 0x78);
}
