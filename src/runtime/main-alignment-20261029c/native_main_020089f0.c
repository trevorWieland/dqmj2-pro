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
extern u32 native_fn_01ff8448();
extern u32 native_fn_02005c64();
extern u32 native_fn_02005d80();
extern u32 native_fn_02008a9c();
extern u8 native_data_020e3740[] __attribute__((aligned(2)));
u32 native_main_020089f0(void) {
    u32 temp_r1;
    s32 temp_r4;
    u32 var_r5;

    var_r5 = M2C_FIELD(native_data_020e3740, u32 *, 0xC);
    if (var_r5 == 0) {
        return (u32) native_data_020e3740;
    }
    if (var_r5 >= 0x1D8U) {
        var_r5 = 0x1D8;
    }
    temp_r4 = M2C_FIELD(native_data_020e3740, s32 *, 8);
    temp_r1 = M2C_FIELD(native_data_020e3740, u32 *, 0xC) - var_r5;
    M2C_FIELD(native_data_020e3740, u32 *, 0xC) = temp_r1;
    M2C_FIELD(native_data_020e3740, s32 *, 8) = (s32) (temp_r4 + var_r5);
    if (temp_r1 == 0) {
        native_fn_02005c64(M2C_FIELD(native_data_020e3740, s32 *, 4), native_fn_02008a9c, 0);
        native_fn_01ff8448(M2C_FIELD(native_data_020e3740, s32 *, 4), temp_r4, 0x04000400, -0x3BC00000 | (var_r5 >> 2));
        return (u32) native_fn_02005d80(0x200000);
    }
    native_fn_01ff8448(M2C_FIELD(native_data_020e3740, s32 *, 4), temp_r4, 0x04000400, 0x84400000 | (var_r5 >> 2));
    return (u32) native_fn_02005d80(0x200000);
}
