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
extern u32 native_fn_01ff8580();
extern u32 native_fn_02008c58();
extern u32 native_fn_0200f3e0();
extern u32 native_fn_0202a37c();
extern u32 native_fn_02041538();
extern u32 native_fn_02048034();
extern u32 native_fn_02048094();
extern u32 native_fn_02063f6c();
extern u32 native_fn_020642cc();
extern u32 native_fn_020642dc();
extern u32 native_fn_02064340();
extern u32 native_fn_02089804();
extern u32 native_fn_02089aa4();
extern u32 native_fn_020bef48();
extern u32 native_fn_020bef58();
extern u32 native_fn_020bf084();
extern u32 native_fn_020bf218();
extern u32 native_fn_020bf4d4();
extern u32 native_fn_ov005_021decb0();
extern u32 native_fn_ov005_021dfacc();
extern u32 native_fn_ov005_021e00b4();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0708();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0de0();
extern u32 native_fn_ov005_021e0df8();
extern u32 native_fn_ov005_021e0e28();
extern u32 native_fn_ov005_021e0fb0();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
extern u32 native_data_ov005_021e7764[];
extern u8 native_data_ov005_021ed438[];
extern u8 native_data_ov005_021ed484[];
extern u32 native_data_ov005_021ed494[];
extern u8 native_data_ov005_021edfe0[];
