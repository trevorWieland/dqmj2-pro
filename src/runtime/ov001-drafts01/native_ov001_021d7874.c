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
    u8 unknown_0[0x748];
    u32 field_748;
    s32 field_74c;
    s32 field_750;
} Record_native_data_ov001_02230d50;
extern Record_native_data_ov001_02230d50 native_data_ov001_02230d50;
u32 native_ov001_021d7874(u32 arg0, s32 arg1, s32 arg2) {
    native_data_ov001_02230d50.field_748 = arg0;
    native_data_ov001_02230d50.field_74c = arg1;
    native_data_ov001_02230d50.field_750 = arg2;
    return arg0;
}
