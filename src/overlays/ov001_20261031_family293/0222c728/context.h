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
extern u32 native_fn_ov001_021d9494();
extern void * native_fn_ov001_021db438(s32, u32);
extern u32 native_fn_ov001_021db7cc();
extern u32 native_fn_ov001_021db8d0(u8 *);
extern u32 native_fn_ov001_021ee7d4();
extern u32 native_fn_ov001_022024d4();
extern u32 native_fn_ov001_0222c024();
extern u32 native_fn_ov001_0222c700();
typedef struct {
    u8 field_0;
    s8 field_1;
    u8 field_2;
    u8 field_3;
} Record_native_data_ov001_022497e8;
extern Record_native_data_ov001_022497e8 native_data_ov001_022497e8;
