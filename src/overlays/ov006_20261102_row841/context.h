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
extern u32 native_fn_02046af4();
extern u32 native_fn_02048094();
extern u32 native_fn_02063eec();
extern u32 native_fn_020643fc(u32 arg0);
extern u32 native_fn_02067b48();
extern u32 native_fn_02067bd4(u32 arg0);
extern u32 native_fn_02067d54(u32 arg0);
extern u32 native_fn_ov006_021d79e4();
extern u32 native_fn_ov006_021d7ad0(u32 arg0, u32 arg1);
extern u32 native_fn_ov006_021d7e34();
extern u32 native_fn_ov006_021d7ebc(u32 arg0, u32 arg1, u32 arg2);
extern u32 native_fn_ov006_021dc08c();
extern u32 native_fn_ov006_021de1a8();
extern u32 native_fn_ov006_021de228();
extern u8 native_data_021c9698[];
extern u8 native_data_ov006_0220f3b8[];
