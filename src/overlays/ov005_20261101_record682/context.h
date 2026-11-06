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
extern u32 native_fn_02008c58();
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
extern f32 native_fn_02024e0c(f32,f32);
extern f32 native_fn_02025578(f32,f32);
extern s32 native_fn_020259b4(f32);
extern f32 native_fn_02025a70(u32);
extern f32 native_fn_02025ab8(f32,f32);
extern u32 native_fn_020449d4();
extern u32 native_fn_0206485c();
extern u32 native_fn_020cf620();
extern u32 native_fn_020cf658();
extern u32 native_fn_ov005_021e1014();
extern u32 native_fn_ov005_021e65ec();
extern u32 native_fn_ov005_021e664c();
extern u32 native_fn_ov005_021e6660();
extern u32 native_fn_ov005_021e6678();
extern u32 native_fn_ov005_021e6aec();
extern u32 native_fn_ov005_021e6b20();
extern u8 native_data_ov005_021ed438[];

typedef struct {u8 first; u8 second;} NativePair;
