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
extern u32 native_fn_02008070();
extern u32 native_fn_02097470(u32);
extern u32 native_fn_0209747c(void);
extern u32 native_fn_ov006_021f4fc0();
extern u32 native_fn_ov006_021f5010();
extern u32 native_fn_ov006_021f50b0();
extern u32 native_fn_ov006_021f527c();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f5870();
extern u32 native_fn_ov006_021ff628();
extern u32 native_fn_ov006_02203cf0();
extern u32 native_fn_ov006_02204150();
extern u32 native_fn_ov006_022047ac();
extern u32 native_fn_ov006_022048a8();
extern u8 native_data_ov006_0220d974[];
extern u8 native_data_ov006_0221c06c[];
