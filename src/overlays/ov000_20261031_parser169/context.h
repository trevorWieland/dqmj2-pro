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
extern u32 native_fn_0201d914(void *, void *, s32);
extern u32 native_fn_0201f274(u32);
extern float native_fn_02024e0c(float, float);
extern s32 native_fn_020259b4(float);
extern float native_fn_02025a28(s32);
extern float native_fn_02025ca4(float, float);
extern u32 native_fn_020282a8(void *, s32);
extern u32 native_fn_ov000_021d8a08();
extern u32 native_fn_ov000_021d8b24();
extern u32 native_fn_ov000_021e3444();
extern u32 native_fn_ov000_021e3478();
extern u8 native_data_ov000_0222ec40[];
extern u8 native_data_ov000_0222ec48[];
extern u8 native_data_ov000_02234388[];
