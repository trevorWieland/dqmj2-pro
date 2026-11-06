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
extern u32 native_fn_020444ec();
extern u32 native_fn_0204453c();
extern u32 native_fn_ov001_021db8b8();
extern u32 native_fn_ov001_021dc3c4();
extern u32 native_fn_ov001_021dda00();
extern u32 native_fn_ov001_021e66f8();
extern u32 native_fn_ov001_021f1c28();
extern u32 native_fn_ov001_02215284();
extern u8 native_data_ov001_022388ec[];
