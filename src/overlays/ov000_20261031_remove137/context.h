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
extern u32 native_fn_020627a0(s32);
extern u32 native_fn_020628b0();
extern u32 native_fn_02062980();
extern u32 native_fn_02062a50();
extern u32 native_fn_02062a88();
extern u32 native_fn_02062aa0();
extern u32 native_fn_02062ad0();
extern u32 native_fn_ov000_021f51d4();
extern u32 native_fn_ov000_02223d58();
extern u32 native_fn_ov000_02223e40();
typedef struct {
    u8 unknown_0[0x1d];
    s8 field_1d;
    s8 field_1e;
} Record_native_data_ov000_022468b8;
extern Record_native_data_ov000_022468b8 native_data_ov000_022468b8;
extern u8 native_data_ov000_02246c84[];
