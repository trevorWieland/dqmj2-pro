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
extern u32 native_fn_02008d78();
extern u8 native_data_ov001_022355e4[];
extern u8 native_data_ov001_022355e8[];
extern u8 native_data_ov001_022355ec[];
extern u8 native_data_ov001_022362ac[];
extern u8 native_data_ov001_02236f6c[];
extern u8 native_data_ov001_02237c2c[];
u32 native_ov001_021d9710(void) {
    s32 var_r1;
    u8 *var_r2;
    u8 *var_r3;

    var_r2 = native_data_ov001_022362ac;
    var_r3 = native_data_ov001_022355e8;
    var_r1 = 0;
    do {
        var_r1 += 1;
        *var_r3 = M2C_FIELD(var_r2, u8 *, 0x35B);
        var_r3 += 1;
        var_r2 += 0x440;
    } while (var_r1 < 3);
    native_fn_02008d78(native_data_ov001_02236f6c, 0, 0xCC0);
    native_fn_02008d78(native_data_ov001_022362ac, 0, 0xCC0);
    native_fn_02008d78(native_data_ov001_022355ec, 0, 0xCC0);
    native_fn_02008d78(native_data_ov001_02237c2c, 0, 0xCC0);
    M2C_FIELD(native_data_ov001_022355e4, s8 *, 3) = 0;
    M2C_FIELD(native_data_ov001_022355e4, s8 *, 2) = 0;
    M2C_FIELD(native_data_ov001_022355e4, u8 *, 0) = 0;
    M2C_FIELD(native_data_ov001_022355e4, s8 *, 1) = 0;
    return (u32) native_data_ov001_022355e4;
}
