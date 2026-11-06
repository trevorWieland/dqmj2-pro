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
extern u32 native_fn_ov001_021d9494();
extern u32 native_fn_ov001_021d9534();
extern u32 native_fn_ov001_021db618();
extern u32 native_fn_ov001_021e97c0();
extern u32 native_fn_ov001_021e9884();
extern u32 native_fn_ov001_021eaa3c();
extern u32 native_fn_ov001_021f1438();
extern u32 native_fn_ov001_021f14e4();
extern u32 native_fn_ov001_021f949c();
extern u32 native_fn_ov001_02202528();
extern u8 native_data_ov001_0222ec84[];
extern u8 native_data_ov001_02238d7c[];
