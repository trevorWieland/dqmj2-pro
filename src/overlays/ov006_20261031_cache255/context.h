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
extern u32 native_fn_0205e644(void);
extern u32 native_fn_0205e66c(void);
extern u32 native_fn_0205e73c(u32);
extern u32 native_fn_0205e7a8(u32, u32);
extern u32 native_fn_0205e814(u32, u32, u32);
typedef struct {
    u8 unknown_0[0x54];
    s32 field_54;
    u32 field_58;
} Record_native_data_ov006_0220f594;
extern Record_native_data_ov006_0220f594 native_data_ov006_0220f594;
