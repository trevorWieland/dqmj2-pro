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
extern u32 native_fn_0207afec(s32);
extern u32 native_fn_ov001_021e215c();
extern u32 native_fn_ov001_021f521c();
extern u32 native_fn_ov001_02212290();
typedef struct {
    u8 unknown_0[0x1b];
    s8 field_1b;
    u8 unknown_1c[0x3];
    u8 field_1f;
    u8 field_20;
    u8 unknown_21[0x2f];
    u16 field_50;
    u8 unknown_52[0x2e];
    s32 field_80;
    s32 field_84;
} Record_native_data_ov001_0223989c;
extern Record_native_data_ov001_0223989c native_data_ov001_0223989c;
