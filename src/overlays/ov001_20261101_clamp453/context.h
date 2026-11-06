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
extern void *native_fn_02062a10(u32);
extern s32 native_fn_ov001_021e8e34(s32,s32,s32,s32,s32,s32);
extern s32 native_fn_ov001_021e8ebc(s32,s32,s32,s32,s32,s32);
extern s32 native_fn_ov001_021e8f44(s32,s32,s32,s32,s32,s32);
extern s32 native_fn_ov001_021e8fcc(s32,s32,s32,s32,s32,s32);
extern s32 native_fn_ov001_021e9054(s32,s32,s32,s32,s32,s32);
extern s32 native_fn_ov001_021e90dc(s32,s32,s32,s32,s32,s32);
