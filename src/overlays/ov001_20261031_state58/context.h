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
extern u32 native_fn_02041510();
extern u32 native_fn_02041800();
extern u32 native_fn_ov001_021d8cc8();
extern u32 native_fn_ov001_021e3564();
extern u32 native_fn_ov001_021e3584();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f949c();
extern u32 native_fn_ov001_021f989c();
typedef struct {
    u8 unknown_0[0x2];
    u8 field_2;
    u8 unknown_3[0x5];
    u8 field_8;
    u8 field_9;
    s8 field_a;
    u8 field_b;
    u8 unknown_c[0x7];
    u8 field_13;
    u8 unknown_14[0x5];
    u8 field_19;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
