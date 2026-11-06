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
typedef struct {
    u8 unknown_0[0x1fc];
    s32 field_1fc;
} Record_native_data_ov001_02238ad4;
extern Record_native_data_ov001_02238ad4 native_data_ov001_02238ad4;
u32 native_ov001_021e3508(s32 arg0) {
    s32 temp_r0;
    s32 temp_r3;

    temp_r3 = native_data_ov001_02238ad4.field_1fc;
    temp_r0 = temp_r3 + arg0;
    native_data_ov001_02238ad4.field_1fc = temp_r0;
    if (temp_r0 > 0xF423F) {
        native_data_ov001_02238ad4.field_1fc = 0xF423F;
    }
    return (u32) temp_r3;
}
