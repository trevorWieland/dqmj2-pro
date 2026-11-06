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
    u8 unknown_0[0xc];
    s32 field_c;
    u8 unknown_10[0x24];
    u32 field_34;
} Record_native_data_ov006_0220f594;
extern Record_native_data_ov006_0220f594 native_data_ov006_0220f594;
u32 native_ov006_021df948(u32 arg0) {
    native_data_ov006_0220f594.field_34 = arg0;
    native_data_ov006_0220f594.field_c = 1;
    return arg0;
}
