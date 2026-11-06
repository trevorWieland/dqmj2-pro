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
extern u32 native_fn_01ffb50c();
extern u32 native_fn_0201d444();
extern u32 native_fn_0203cc2c(u32, u32);
extern u32 native_fn_02061c1c(u32, s32, s32, s32, s32, s8, s8);
extern u8 native_data_ov000_0222f2f0[];
typedef struct {
    u8 unknown_0[0x2];
    s8 field_2;
    u8 unknown_3[0x19];
    u32 field_1c;
    s32 field_20;
} Record_native_data_ov000_02236ee4;
extern Record_native_data_ov000_02236ee4 native_data_ov000_02236ee4;
