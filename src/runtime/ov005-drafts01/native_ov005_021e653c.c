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
extern u32 native_fn_02008c58();
extern u32 native_fn_020bf028();
extern u32 native_fn_ov005_021e63e8();
extern u32 native_fn_ov005_021e6b30();
extern u8 native_data_ov005_021ed438[];
extern u8 native_data_ov005_021edaf4[];
u32 native_ov005_021e653c(void) {
    switch (M2C_FIELD(native_data_ov005_021ed438, u8 *, 6)) {
    case 7:
        native_fn_02008c58(0, native_data_ov005_021edaf4, 0x268);
        native_fn_ov005_021e6b30();
        native_fn_020bf028(native_data_ov005_021edaf4, 7);
        break;
    case 8:
        native_fn_02008c58(0, native_data_ov005_021edaf4, 0x268);
        native_fn_ov005_021e63e8(5);
        native_fn_020bf028(native_data_ov005_021edaf4, 8);
        break;
    case 9:
        native_fn_02008c58(0, native_data_ov005_021edaf4, 0x268);
        native_fn_ov005_021e63e8(6);
        native_fn_020bf028(native_data_ov005_021edaf4, 9);
        break;
    }
    M2C_FIELD(native_data_ov005_021ed438, u8 *, 6) = 0U;
    return (u32) native_data_ov005_021ed438;
}
