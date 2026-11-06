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
extern u32 native_fn_020bb38c();
extern u32 native_fn_020bb3cc();
extern u8 native_data_ov005_021e73c4[];
extern u8 native_data_ov005_021e73d0[];
extern u8 native_data_ov005_021e73e0[];
extern u8 native_data_ov005_021e73f4[];
extern u8 native_data_ov005_021e7400[];
extern u8 native_data_ov005_021e7410[];
extern u8 native_data_ov005_021e741c[];
extern u8 native_data_ov005_021e742c[];
typedef struct {
    u8 unknown_0[0x38];
    u32 field_38;
} Record_native_data_ov005_021e9818;
extern Record_native_data_ov005_021e9818 native_data_ov005_021e9818;
u32 native_ov005_021ddc48(u32 arg0) {
    u8 sp0[32];

    if (native_data_ov005_021e9818.field_38 != 0) {
        native_fn_020bb38c(native_data_ov005_021e9818.field_38, 1);
    }
    switch (arg0) {
    default:
        break;
    case 2:
        native_fn_0201d444(&sp0, native_data_ov005_021e73c4);
        break;
    case 3:
        native_fn_0201d444(&sp0, native_data_ov005_021e73d0);
        break;
    case 4:
        native_fn_0201d444(&sp0, native_data_ov005_021e73e0);
        break;
    case 5:
        native_fn_0201d444(&sp0, native_data_ov005_021e73f4);
        break;
    case 6:
        native_fn_0201d444(&sp0, native_data_ov005_021e7400);
        break;
    case 7:
        native_fn_0201d444(&sp0, native_data_ov005_021e7410);
        break;
    case 8:
        native_fn_0201d444(&sp0, native_data_ov005_021e741c);
        break;
    case 9:
        native_fn_0201d444(&sp0, native_data_ov005_021e742c);
        break;
    }
    native_data_ov005_021e9818.field_38 = native_fn_020bb338(&sp0, 1);
    return native_fn_020bb3cc();
}
