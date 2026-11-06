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
extern u32 native_fn_020bf4c4();
extern u32 native_fn_ov005_021dd788();
extern u32 native_fn_ov005_021ddf24();
extern u32 native_fn_ov005_021de19c();
extern u32 native_fn_ov005_021e0040();
extern u32 native_fn_ov005_021e026c();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e0a90();
extern u32 native_fn_ov005_021e0d88();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e155c();
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
    u8 unknown_5[0x3b];
    s32 field_40;
    u8 unknown_44[0x4];
    s32 field_48;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
