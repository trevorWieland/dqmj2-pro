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
extern u32 native_fn_02008e0c();
extern u32 native_fn_0208b580();
extern u8 native_data_020de7b4[];
extern u8 native_data_021cfcf8[];
u32 native_main_0208bce8(s32 arg0, s32 arg1, u32 arg2, s32 arg3) {
    u8 var_r1;

    native_fn_02008e0c(native_data_020de7b4, arg0 + 6, 6);
    if ((s32) native_fn_0208b580(arg0, arg0 + 6, arg1 - 6, arg2, arg3) < 0) {
        var_r1 = 1;
    } else {
        var_r1 = 0;
    }
    *native_data_021cfcf8 = var_r1;
    return (u32) native_data_021cfcf8;
}
