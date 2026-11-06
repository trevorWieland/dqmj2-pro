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
extern u32 native_fn_02002480();
extern u32 native_fn_ov006_021fac5c();
extern u32 native_fn_ov006_021fad68();
extern u32 native_fn_ov006_021fb080();
extern u32 native_fn_ov006_021fe4fc();
extern u32 native_fn_ov006_021fe510();
extern u32 native_fn_ov006_0220383c();
extern u32 native_fn_ov006_022038ac();
extern u16 native_data_ov006_0220b73e[];
extern u8 native_data_ov006_0221c0ec[];
