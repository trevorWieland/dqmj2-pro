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
#define NULL ((void *)0)
typedef struct {
    u8 unknown_0[0x4];
    s32 field_4;
    s32 field_8;
    u8 unknown_c[0x14];
    u32 field_20;
} Record_native_data_ov003_021e0d18;
extern Record_native_data_ov003_021e0d18 native_data_ov003_021e0d18;
u32 native_ov003_021dfd50(u32 arg0, s32 arg1, s32 arg2) {
    native_data_ov003_021e0d18.field_20 = arg0;
    native_data_ov003_021e0d18.field_8 = arg1;
    native_data_ov003_021e0d18.field_4 = arg2;
    return arg0;
}
