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
extern u32 native_fn_020685f0();
extern u32 native_fn_0206877c();
extern u32 native_fn_ov006_021e749c();
extern u32 native_fn_ov006_021e75ec();
extern u32 native_fn_ov006_021e775c(s32,void*,s32,s32,u32,u32,u32);
extern u32 native_fn_ov006_021e7824(u32,void*,s32,s32,u32,u32,u32);
extern u32 native_fn_ov006_021e78ac(u32,u32,s32,s32,u32,u32,u32,u32);
extern u32 native_fn_ov006_021e791c(u32,void*,s32,s32,u32,u32,u32);
extern u32 native_fn_ov006_021e796c();
extern u32 native_fn_ov006_021e7b64();
extern u32 native_fn_ov006_021e92bc();
extern u32 native_fn_ov006_0220769c();
extern u8 native_data_ov006_022084f8[];
extern u8 native_data_ov006_02208504[];
extern u8 native_data_ov006_02208510[];
extern u8 native_data_ov006_02208514[];
extern u8 native_data_ov006_02208518[];
extern u8 native_data_ov006_0220d3b8[];
extern u8 native_data_ov006_0220d3d0[];
extern u8 native_data_ov006_0220d3d4[];
