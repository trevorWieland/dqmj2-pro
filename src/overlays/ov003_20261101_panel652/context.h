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
extern u32 native_fn_02045dc4();
extern u32 native_fn_02048f5c();
extern u32 native_fn_02049008();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0206006c();
extern u32 native_fn_0206b324();
extern u32 native_fn_020851d4();
extern u32 native_fn_02085200();
extern u32 native_fn_ov003_021de71c();
extern u8 native_data_ov003_021e0a68[];
extern u8 native_data_ov003_021e0a6c[];
extern u8 native_data_ov003_021e0a70[];
extern u8 native_data_ov003_021e0a9c[];
