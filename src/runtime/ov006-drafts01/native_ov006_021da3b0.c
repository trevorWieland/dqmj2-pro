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
extern u32 native_fn_0201d444();
extern u32 native_fn_020bb338();
extern u8 native_data_ov006_0220cd00[];
typedef struct {
    u8 unknown_0[0x8];
    u32 field_8;
} Record_native_data_ov006_0220f33c;
extern Record_native_data_ov006_0220f33c native_data_ov006_0220f33c;
u32 native_ov006_021da3b0(void) {
    u32 temp_r0;
    u8 sp0[32];

    native_fn_0201d444(&sp0, native_data_ov006_0220cd00);
    temp_r0 = native_fn_020bb338(&sp0, 1);
    native_data_ov006_0220f33c.field_8 = temp_r0;
    return temp_r0;
}
