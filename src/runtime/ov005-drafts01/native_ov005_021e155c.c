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
extern u32 native_fn_020bf014();
extern u32 native_fn_ov005_021e00b4();
typedef struct {
    u8 unknown_0[0x4];
    u8 field_4;
    u8 unknown_5[0x5b];
    u32 field_60;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
u32 native_ov005_021e155c(u32 arg0) {
    u8 temp_r0;

    native_data_ov005_021ed438.field_60 = arg0;
    if (arg0 != 0xD) {
        return arg0;
    }
    temp_r0 = M2C_FIELD((void *) native_fn_020bf014(native_data_ov005_021ed438.field_4), u8 *, 0xAF);
    switch (temp_r0) {
    case 7:
        return native_fn_ov005_021e00b4(0x13, 0U, 0x1F, 3);
    case 8:
        return native_fn_ov005_021e00b4(0x13, 0U, 0x20, 3);
    case 9:
        return native_fn_ov005_021e00b4(0x13, 0U, 0x21, 3);
    default:
        return native_fn_ov005_021e00b4(0xFF, native_data_ov005_021ed438.field_4, 1, 2);
    }
}
