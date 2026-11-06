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
extern u32 native_fn_0205e73c();
extern u32 native_fn_0205e7a8();
extern u32 native_fn_0205f5dc();
typedef struct {
    u32 field_0;
    u8 unknown_4[0x10];
    u32 field_14;
} Record_native_data_ov006_0220f4e8;
extern Record_native_data_ov006_0220f4e8 native_data_ov006_0220f4e8;
u32 native_ov006_021de2e8(u32 arg0) {
    u32 temp_r0;

    native_data_ov006_0220f4e8.field_14 = native_fn_0205f5dc();
    native_fn_0205e73c(arg0);
    temp_r0 = native_fn_0205e7a8(-1, arg0);
    native_data_ov006_0220f4e8.field_0 = temp_r0;
    return temp_r0;
}
