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
extern u32 native_fn_020273c8(void);
extern void native_fn_020404f0(s8);
extern void native_fn_020407a8(void);
extern u32 native_fn_02041538(u32, u32, u32);
extern u32 native_fn_0204157c();
extern u8 native_fn_02048f7c(u32);
extern u32 native_fn_0205e7a8(u32, u32);
extern u32 native_fn_020620e8(s8, u32);
extern u8 *native_fn_02062a10(u32);
extern u32 native_fn_02068f60(s8);
extern u32 native_fn_020698f4();
extern u32 native_fn_0206a04c(void);
extern u32 native_fn_0206bf44();
extern u32 native_fn_0206dcd0(void *);
#include "../../../api.h"
extern u32 native_fn_020c48bc(void);
extern u32 native_fn_020c48d0(s8, s8, s16);
extern u32 native_fn_020c48e8(u32);
extern u32 native_fn_ov000_021ead88();
extern u32 native_fn_ov000_021eadd0();
extern u32 native_fn_ov000_0221c000();
extern u32 native_fn_ov000_0221c6e4();
extern u32 native_fn_ov000_0221e6cc();
extern u32 native_fn_ov000_0221e7e8();
extern u32 native_fn_ov000_0221ebf4();
extern u32 native_fn_ov000_0221fbb8();
extern u32 native_fn_ov000_02220278();
extern u32 native_fn_ov000_02220778();
extern u32 native_fn_ov000_022207a0(void *, s32);
extern u32 native_fn_ov000_02221154();
extern u32 native_fn_ov000_022212b8();
extern u32 native_fn_ov000_022212f0();
extern u32 native_fn_ov000_02221344();
extern u32 native_fn_ov000_02221358();
extern u8 * native_fn_ov000_02229100(u32,u32,u32,u32,u32);
extern u32 native_fn_ov000_022298ec();
extern u8 native_data_ov000_02246090[];
extern u8 native_data_ov000_022460b4[];
extern u8 native_data_ov000_022460d4[];
