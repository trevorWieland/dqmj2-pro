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
extern u32 native_fn_02048034();
extern u32 native_fn_020bef68();
extern u32 native_fn_020bf224();
extern u32 native_fn_ov005_021dd6c0();
extern u32 native_fn_ov005_021e155c();
extern u32 native_fn_ov005_021e5b60();
extern u8 native_data_ov005_021ed438[];
extern u8 native_data_ov005_021edaf4[];
extern u8 native_data_ov005_021edba4[];
u32 native_ov005_021e2cd8(void) {
    native_fn_020bf224(native_data_ov005_021edaf4, M2C_FIELD(native_data_ov005_021edaf4, u8 *, 0xAF));
    switch (M2C_FIELD(native_data_ov005_021edaf4, u8 *, 0xAF)) {
    case 1:
        native_fn_020bef68(0);
        native_fn_02048034(native_data_ov005_021edba4, 0);
        M2C_FIELD(native_data_ov005_021ed438, s16 *, 0xA) = 4;
        M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64) = 0x14;
        native_fn_ov005_021e5b60();
        native_fn_ov005_021dd6c0(1);
        break;
    case 3:
        native_fn_020bef68(1);
        native_fn_02048034(native_data_ov005_021edba4, 0);
        M2C_FIELD(native_data_ov005_021ed438, s16 *, 0xA) = 4;
        M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64) = 0x14;
        native_fn_ov005_021e5b60();
        native_fn_ov005_021dd6c0(3);
        break;
    case 2:
        native_fn_020bef68(2);
        native_fn_02048034(native_data_ov005_021edba4, 0);
        M2C_FIELD(native_data_ov005_021ed438, s16 *, 0xA) = 5;
        M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64) = 0x14;
        native_fn_ov005_021e5b60();
        native_fn_ov005_021dd6c0(1);
        break;
    default:
        native_fn_020bef68(4);
        native_fn_02048034(native_data_ov005_021edba4, 0);
        M2C_FIELD(native_data_ov005_021ed438, s32 *, 0x64) = 0x15;
        native_fn_ov005_021e5b60();
        switch (M2C_FIELD(native_data_ov005_021edaf4, u8 *, 0xAF)) {
        case 7:
            M2C_FIELD(native_data_ov005_021ed438, s16 *, 0xA) = 0x16;
            native_fn_ov005_021dd6c0(7);
            break;
        case 8:
            M2C_FIELD(native_data_ov005_021ed438, s16 *, 0xA) = 0x14;
            native_fn_ov005_021dd6c0(8);
            break;
        case 9:
            M2C_FIELD(native_data_ov005_021ed438, s16 *, 0xA) = 0x15;
            native_fn_ov005_021dd6c0(9);
            break;
        }
        break;
    }
    native_fn_ov005_021e155c(0x13);
    M2C_FIELD(native_data_ov005_021ed438, s8 *, 2) = 0;
    return (u32) native_data_ov005_021ed438;
}
