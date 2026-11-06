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
extern u32 native_fn_020630e4();
extern u32 native_fn_02065dec();
extern u32 native_fn_ov001_0220b770();
typedef struct {
    u8 unknown_0[0x3];
    s8 field_3;
} Record_native_data_ov001_0223e088;
extern Record_native_data_ov001_0223e088 native_data_ov001_0223e088;
u32 native_ov001_0220d1f0(void) {
    u32 temp_r4;

    temp_r4 = native_fn_ov001_0220b770();
    if (native_fn_02065dec() != 0) {
        native_fn_020630e4(temp_r4, -1);
    }
    native_data_ov001_0223e088.field_3 = 5;
    return 1U;
}
