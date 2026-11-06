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
extern u32 native_fn_020037dc();
extern u32 native_fn_02003cf8(void);
extern u32 native_fn_02003d0c(void);
extern u32 native_fn_02003d20(void);
extern u32 native_fn_02003d44(void);
extern u32 native_fn_02003d68(void);
extern u32 native_fn_02003d7c(void);
extern u32 native_fn_02003d90(void);
extern u32 native_fn_02003da4(void);
extern u32 native_fn_02003db8(void);
extern u32 native_fn_02003dcc(void);
extern u32 native_fn_02003de0(void);
extern u32 native_fn_02003df4(void);
extern u32 native_fn_02003e1c(void);
extern u32 native_fn_ov006_02204740();
typedef struct {
    u32 field_0;
    u32 field_4;
    u32 field_8;
    u32 field_c;
    u32 field_10;
    u32 field_14;
    u32 field_18;
    u32 field_1c;
    u32 field_20;
    u32 field_24;
    u32 field_28;
    u32 field_2c;
    u32 field_30;
} Record_native_data_ov006_0221c1b4;
extern Record_native_data_ov006_0221c1b4 native_data_ov006_0221c1b4;
