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
extern u32 native_fn_0202ac08();
extern u32 native_fn_0202ac4c();
extern u32 native_fn_0205c904();
extern u32 native_fn_0205d6f4();
extern u8 *native_fn_0207afec(u32);
extern u32 native_fn_ov001_021d7f54();
extern u32 native_fn_ov001_021eea10();
extern u32 native_fn_ov001_021eeb70();
extern u32 native_fn_ov001_021f1354();
extern u32 native_fn_ov001_021f1414();
extern u32 native_fn_ov001_021f1438();
extern u32 native_fn_ov001_021f14a4();
extern u32 native_fn_ov001_0222bf54();
typedef struct {
    u8 unknown_0[0xc];
    u8 field_c;
    u8 field_d;
    s8 field_e;
} Record_native_data_ov001_022497e8;
extern Record_native_data_ov001_022497e8 native_data_ov001_022497e8;
extern u8 native_data_ov001_022497f8[];
