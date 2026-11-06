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
extern u32 native_fn_0205c904(u32 arg0);
extern u32 native_fn_0205d718(u32 arg0);
extern u32 native_fn_0205d790(u32);
extern u32 native_fn_0207afec(u32 arg0);
extern u32 native_fn_0207b004();
extern u32 native_fn_0207b02c();
extern u32 native_fn_0207b244();
extern u32 native_fn_ov001_021d9494(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov001_021d9534(u32 arg0, u32 arg1, u32 arg2, u32 arg3);
extern u32 native_fn_ov001_021db438(u32,u32);
extern u32 native_fn_ov001_021db834();
extern u32 native_fn_ov001_021db8d0(u32);
extern u32 native_fn_ov001_021dbd30(u32 arg0);
extern u32 native_fn_ov001_021dca54(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov001_021dd02c(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov001_021e29e8();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70(u32);
extern u32 native_fn_ov001_021eec7c(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f1414(u32 arg0);
extern u32 native_fn_ov001_021f1438(u32 arg0);
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_021f1d54(u32 arg0);
extern u32 native_fn_ov001_021f94d8(u32 arg0, u32 arg1);
extern u32 native_fn_ov001_022024d4(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov001_02202528();
extern u32 native_fn_ov001_02202540();
extern u8 native_data_ov001_0222ed14[];
extern u8 native_data_ov001_0223989c[];
extern u8 native_data_ov001_0223992c[];
