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
extern u32 native_fn_02041f74();
extern u32 native_fn_02042c2c(u32 arg0);
extern u32 native_fn_02065d88(u32 arg0);
extern u32 native_fn_0207afec(u32 arg0);
extern u32 native_fn_0207b058(u32 arg0, u32 arg1);
extern u32 native_fn_ov001_021d75d4();
extern u32 native_fn_ov001_021d77b0();
extern u32 native_fn_ov001_021d7814(u32 arg0, u32 arg1);
extern u32 native_fn_ov001_021d7e80(u32 arg0);
extern u32 native_fn_ov001_021d9494(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov001_021d94cc(u32 arg0, u32 arg1);
extern u32 native_fn_ov001_021d9534(u32 arg0, u32 arg1, u32 arg2, u32 arg3);
extern u32 native_fn_ov001_021dbaac(u32 arg0);
extern u32 native_fn_ov001_021eaa3c();
extern u32 ov001_select_mode_id_021f1438(u32 arg0);
extern u32 native_fn_ov001_021f949c(u32 arg0, u32 arg1);
extern u8 native_data_ov001_02238d7c[];
