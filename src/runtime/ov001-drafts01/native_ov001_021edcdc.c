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
extern u32 native_fn_ov001_02216ac4();
typedef struct {
    u8 unknown_0[0x12];
    u8 field_12;
    s8 field_13;
    u8 field_14;
    u8 unknown_15[0x4b];
    s32 field_60;
} Record_native_data_ov001_02238d7c;
extern Record_native_data_ov001_02238d7c native_data_ov001_02238d7c;
u32 native_ov001_021edcdc(void) {
    if (native_fn_ov001_02216ac4(native_data_ov001_02238d7c.field_60, native_data_ov001_02238d7c.field_12, native_data_ov001_02238d7c.field_14) != 0) {
        native_data_ov001_02238d7c.field_13 = 0x13;
    }
    return 0U;
}
