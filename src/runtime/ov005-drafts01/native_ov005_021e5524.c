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
extern u32 native_fn_020081fc();
extern u32 native_fn_0201b248();
extern u32 native_fn_ov005_021e1014();
extern u32 native_fn_ov005_021e1074();
extern u32 native_fn_ov005_021e5e8c();
extern u32 native_fn_ov005_021e5f1c();
typedef struct {
    u8 unknown_0[0x10];
    s32 field_10;
    u8 unknown_14[0x18];
    s32 field_2c;
} Record_native_data_ov005_021ed438;
extern Record_native_data_ov005_021ed438 native_data_ov005_021ed438;
extern u8 native_data_ov005_021edaf4[];
extern u8 native_data_ov005_021edb9c[];
typedef struct {
    u8 unknown_0[0x66];
    u16 field_66;
} Record_native_data_ov005_021edcf4;
extern Record_native_data_ov005_021edcf4 native_data_ov005_021edcf4;
u32 native_ov005_021e5524(void) {
    u8 sp0[8];

    if (native_data_ov005_021edcf4.field_66 != native_fn_ov005_021e1014(native_data_ov005_021edaf4)) {
        return 0U;
    }
    if (native_data_ov005_021ed438.field_2c == 1) {
        return 0U;
    }
    if (native_fn_ov005_021e5e8c(native_data_ov005_021ed438.field_10 + 0xA8) == 1) {
        return 0U;
    }
    if (native_fn_ov005_021e1074() == 1) {
        native_fn_ov005_021e5f1c(native_data_ov005_021edb9c);
        return 0U;
    }
    native_fn_020081fc(&sp0);
    if (native_fn_0201b248(&sp0, native_data_ov005_021ed438.field_10 + 0xA8, 6) != 0) {
        return 1U;
    }
    return 0U;
}
