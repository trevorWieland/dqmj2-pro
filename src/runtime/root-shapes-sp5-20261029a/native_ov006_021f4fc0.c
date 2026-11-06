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
    u8 field_0;
    u8 unknown_1[0x7];
    u32 field_8;
} Record_native_data_ov006_0221c06c;
extern Record_native_data_ov006_0221c06c native_data_ov006_0221c06c __attribute__((aligned(2)));
u32 native_ov006_021f4fc0(u8 arg0, u32 arg1) {
    u32 temp_r2;

    native_data_ov006_0221c06c.field_0 = arg0;
    native_data_ov006_0221c06c.field_8 = arg1;
    if (((s32) arg0 < 0) || ((s32) arg0 > 6)) {
        return 0U;
    }
    if ((u32) ((u32) (arg1 << 0x1C) >> 0x1C) > 1U) {
        return 0U;
    }
    temp_r2 = arg1 >> 4;
    if (2 & temp_r2) {
        return 0U;
    }
    if ((arg0 != 0) && (1 & temp_r2)) {
        return 0U;
    }
    if ((arg0 == 0) && !(1 & temp_r2)) {
        return 0U;
    }
    return 1U;
}
