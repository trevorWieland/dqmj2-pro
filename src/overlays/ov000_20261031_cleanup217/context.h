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
extern u32 native_fn_02028dac();
extern u32 native_fn_0202a164();
extern u32 native_fn_0202a498();
extern void native_fn_020406a8(s8);
extern u32 native_fn_020410a8();
extern u32 native_fn_02043070();
extern u32 native_fn_02061898();
extern u32 native_fn_02062328(void);
extern u32 native_fn_0206dec8(void);
extern u32 native_fn_0207aad0();
extern void native_fn_02084920(void);
extern u32 native_fn_ov000_021eaa80();
extern u8 native_data_ov000_02236950[];
