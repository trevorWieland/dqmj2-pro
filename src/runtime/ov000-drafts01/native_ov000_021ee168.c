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
extern u32 native_fn_02062d04();
extern u32 native_fn_02063144();
extern u32 native_fn_0208485c();
u32 native_ov000_021ee168(u32 arg0) {
    u32 var_r4;

    var_r4 = 0;
    if (native_fn_02063144() == 0) {
        var_r4 = 3;
    } else if (native_fn_0208485c(arg0) == 0) {
        var_r4 = 1;
    } else if ((s32) native_fn_02062d04(arg0) <= 0) {
        var_r4 = 2;
    }
    return var_r4;
}
