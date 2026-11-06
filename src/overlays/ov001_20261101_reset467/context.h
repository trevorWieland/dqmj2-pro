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
extern u32 native_fn_0202a498(u32,u32);
extern u32 native_fn_02041814(void);
extern u32 native_fn_02068d54(void);
extern u32 native_fn_ov001_021fd354();
extern u32 native_fn_ov001_021fe54c();
extern u32 native_fn_ov001_02203e60();
extern u32 native_fn_ov001_02204090();
typedef struct {
    u8 unknown_0[0x1];
    s8 field_1;
    u8 unknown_2[0x2];
    s32 field_4;
} Record_native_data_ov001_0223d8ec;
extern Record_native_data_ov001_0223d8ec native_data_ov001_0223d8ec;
