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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_02008430();
extern u32 native_fn_02008c14();
extern u32 native_fn_ov005_021d731c();
extern u32 native_fn_ov005_021d86f0();
extern u32 native_fn_ov005_021d87b4();
extern u32 native_fn_ov005_021d8900();
extern u32 native_fn_ov005_021d90f0();
typedef struct {
    s32 field_0;
    s32 field_4;
} Record_native_data_ov005_021e78cc;
extern Record_native_data_ov005_021e78cc native_data_ov005_021e78cc;
