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
extern u32 native_fn_02002e5c();
extern u32 native_fn_020030ec();
extern u32 native_fn_0200323c();
extern u32 native_fn_0200333c();
extern u32 native_fn_020033e8();
extern u32 native_fn_020035c0();
extern u32 native_fn_020036a8();
extern u32 native_fn_02003888();
extern u32 native_fn_020038a8();
extern u32 native_fn_02003950();
extern u32 native_fn_020039c0();
extern u32 native_fn_02003a40();
extern u32 native_fn_02003cf8(void);
extern u32 native_fn_02003d0c(void);
extern u32 native_fn_02003dcc(void);
extern u32 native_fn_02003de0(void);
extern u32 native_fn_ov006_02204740();
typedef struct {
    s32 field_0;
    s32 field_4;
    s32 field_8;
    s32 field_c;
    s32 field_10;
    s32 field_14;
    s32 field_18;
    s32 field_1c;
    s32 field_20;
    s32 field_24;
    s32 field_28;
    u8 unknown_2c[0x4];
    s32 field_30;
} Record_native_data_ov006_0221c1b4;
extern Record_native_data_ov006_0221c1b4 native_data_ov006_0221c1b4;
