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
extern u32 native_fn_02026144();
u32 native_ov001_021e404c(s32 arg0, s32 arg1, s32 arg2) {
    s32 var_r0;
    s32 var_r2;

    var_r0 = arg0;
    var_r2 = arg2;
    switch (var_r0) {
    case 2:
        var_r0 = 2;
        var_r2 = 1;
        break;
    case 0:
        var_r0 = 1;
        var_r2 = 1;
        break;
    case 1:
        var_r0 = 3;
        var_r2 = 2;
        break;
    }
    return (u32) (s16) native_fn_02026144(arg1 * var_r0, var_r2);
}
