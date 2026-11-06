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
    u8 unknown_0[0x4];
    s32 field_4;
    u8 unknown_8[0x4];
    u32 field_c;
    u8 unknown_10[0x8];
    s32 field_18;
} Record_native_data_ov006_0220f3b8;
extern Record_native_data_ov006_0220f3b8 native_data_ov006_0220f3b8;
u32 native_ov006_021db59c(u32 arg0, s32 arg1, s32 arg2) {
    native_data_ov006_0220f3b8.field_c = arg0;
    native_data_ov006_0220f3b8.field_18 = arg1;
    native_data_ov006_0220f3b8.field_4 = arg2;
    return arg0;
}
