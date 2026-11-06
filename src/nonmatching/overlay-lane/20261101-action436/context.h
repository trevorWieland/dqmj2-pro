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
extern u32 native_fn_02008d78();
extern u32 native_fn_0203d294(s32);
extern u32 native_fn_02044cdc();
extern u32 native_fn_02065d88();
extern u32 native_fn_0207afec(s32);
extern u32 native_fn_0207b004();
extern u32 native_fn_0207b244();
extern void * native_fn_ov001_021db438(s32, u32);
extern u32 native_fn_ov001_021db834();
extern u32 native_fn_ov001_021db8d0(u8 *);
extern u32 native_fn_ov001_021db9f4(void *);
extern s32 native_fn_ov001_021dbd30(u8 *);
extern u32 native_fn_ov001_021e1358();
extern u32 native_fn_ov001_021e19c8();
extern u32 native_fn_ov001_021e9cbc();
extern u32 native_fn_ov001_021f0bec();
extern u32 native_fn_ov001_021f0c40();
extern u32 native_fn_ov001_021f1294();
extern u32 native_fn_ov001_021f1414();
extern u32 native_fn_ov001_021f2304();
extern u32 native_fn_ov001_022024d4();
extern u32 native_fn_ov001_02202568();
extern u32 native_fn_ov001_0220f9a4();
extern u8 native_data_ov001_0222ec84[];
extern u8 native_data_ov001_02238d7c[];
extern u8 native_data_ov001_02238d8e[];
