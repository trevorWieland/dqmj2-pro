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
extern u32 native_fn_0202ac08();
extern u32 native_fn_0202ac4c();
extern u32 native_fn_02041510(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_02041800();
extern u32 native_fn_0205c904(u32 arg0);
extern u32 native_fn_ov001_021db438(u32,u32);
extern u32 native_fn_ov001_021db8d0(void *);
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70(u32);
extern s32 native_fn_ov001_021eec7c(u32 arg0, u8 *arg1, s32 arg2);
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_021f949c(u32 arg0, u32 arg1);
extern u32 native_fn_ov001_021f94d8(u32 arg0, u32 arg1);
extern u32 native_fn_ov001_021f9ac8();
extern u8 native_data_ov001_02239a14[];
extern u8 native_data_ov001_02239a5c[];
