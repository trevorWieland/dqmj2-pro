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
extern u32 native_fn_0205e844();
extern u8 *native_fn_ov005_021decb0(void);
extern u32 native_fn_ov005_021dfd70();
extern u32 native_fn_ov005_021e09dc();
extern u8 *native_fn_ov005_021e0a68(void);
extern u32 native_fn_ov005_021e4e48();
extern u32 native_fn_ov005_021e4e80();
extern u32 native_fn_ov005_021e5dcc();
extern u32 (*native_data_ov005_021e7778[])(void);
typedef struct {
    u8 unknown_0[0x14];
    u32 field_14;
    u8 unknown_18[0x44];
    u32 field_5c;
    u32 field_60;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
