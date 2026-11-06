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
extern void **native_fn_02049ad0(s32);
extern u32 native_fn_02049f4c();
extern void native_fn_02049ffc();
extern u32 native_fn_0204a154();
extern u32 native_fn_0204a724();
extern u32 native_fn_0204a808();
extern u32 native_fn_020602ec();
extern u32 native_fn_02062aa0();
extern u32 native_fn_02063fa0();
extern u32 native_fn_02063fac();
extern u32 native_fn_02065818();
extern u32 native_fn_ov000_0221742c();
__declspec(align(4)) extern u8 native_data_020de410[];
__declspec(align(4)) extern u8 native_data_021c6234[];
