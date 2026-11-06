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
extern u32 native_fn_ov001_021e3564();
extern u32 native_fn_ov001_021e3584();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_0220b770();
extern u32 native_fn_ov001_0220b8b4();
typedef struct {
    u8 field_0;
    u8 unknown_1[0x2];
    s8 field_3;
    u8 unknown_4[0x12];
    u8 field_16;
} Record_native_data_ov001_0223e088;
extern Record_native_data_ov001_0223e088 native_data_ov001_0223e088;
