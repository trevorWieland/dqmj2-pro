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
extern u32 native_fn_0207afec();
extern u32 native_fn_0207b02c();
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021db8d0();
extern u32 native_fn_ov001_021db918();
extern u32 native_fn_ov001_021dc108();
extern u32 native_fn_ov001_021dc138();
extern u32 native_fn_ov001_021dcb90();
extern u32 native_fn_ov001_021dd108();
extern u32 native_fn_ov001_021e29d8();
extern u32 native_fn_ov001_021e8178();
extern u32 native_fn_ov001_021e81d0();
extern u32 native_fn_ov001_021e8424();
extern u32 native_fn_ov001_021e8510();
extern u32 native_fn_ov001_021e85f4();
extern u32 native_fn_ov001_021e865c();
extern u32 native_fn_ov001_021e95d8();
extern u32 native_fn_ov001_021e97a4();
extern u32 native_fn_ov001_021f1bf0();
extern u32 native_fn_ov001_0220b770();
extern u32 native_fn_ov001_022142d0();
extern u32 native_fn_ov001_02214308();
extern u32 native_fn_ov001_022148a0();
extern u32 native_fn_ov001_02215274();
extern u32 native_fn_ov001_0221689c();
extern u32 native_fn_ov001_02217a7c();
typedef struct {
    u8 unknown_0[0x7];
    u8 field_7;
    s8 field_8;
    u8 unknown_9[0x1];
    s8 field_a;
    u8 unknown_b[0x1];
    u8 field_c;
    u8 unknown_d[0x4];
    s8 field_11;
    s8 field_12;
    u8 unknown_13[0x4];
    u8 field_17;
    s8 field_18;
    s8 field_19;
    s8 field_1a;
    u8 field_1b;
    u8 unknown_1c[0x1];
    u8 field_1d;
    u8 unknown_1e[0x18];
    u16 field_36;
    u8 unknown_38[0x8];
    u32 field_40;
    u8 unknown_44[0x4];
    u32 field_48;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
