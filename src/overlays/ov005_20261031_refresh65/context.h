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
extern u32 native_fn_02048094();
extern u32 native_fn_02049604();
extern u32 native_fn_020bf084();
extern u32 native_fn_ov005_021e0730();
extern u32 native_fn_ov005_021e0818();
extern u32 native_fn_ov005_021e085c();
extern u32 native_fn_ov005_021e0a68();
extern u32 native_fn_ov005_021e0a84();
extern u32 native_fn_ov005_021e1048();
extern u32 native_fn_ov005_021e1144();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e6004();
extern u32 native_fn_ov005_021e653c();
typedef struct {
    u8 unknown_0[0x1];
    u8 field_1;
    s8 field_2;
    u8 unknown_3[0x9];
    s16 field_c;
    u8 unknown_e[0x12];
    s32 field_20;
    u8 unknown_24[0x10];
    s32 field_34;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
