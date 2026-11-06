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
extern u32 native_fn_02084f4c();
extern u32 native_fn_ov005_021db134();
extern u8 native_data_ov005_021e9818[];
extern u8 native_data_ov005_021e992c[];
u32 native_ov005_021dbaa4(void) {
    s8 var_r5;
    s8 var_r5_2;

    switch (M2C_FIELD(native_data_ov005_021e9818, s8 *, 0x66)) {
    case 0:
        var_r5 = 0;
        do {
            native_fn_02084f4c(*(u32 *)(native_data_ov005_021e992c + (var_r5 * 4)));
            var_r5 += 1;
        } while ((s32) var_r5 < 0xF);
        break;
    case 1:
        var_r5_2 = 0;
        do {
            native_fn_02084f4c(*(u32 *)(native_data_ov005_021e992c + (var_r5_2 * 4)));
            var_r5_2 += 1;
        } while ((s32) var_r5_2 < 0xE);
        break;
    }
    native_fn_ov005_021db134();
    M2C_FIELD(native_data_ov005_021e9818, s8 *, 0x66) = -1;
    return (u32) native_data_ov005_021e9818;
}
