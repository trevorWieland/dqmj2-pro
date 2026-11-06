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
extern u32 native_fn_0208d9a0();
extern u32 native_fn_0208da30();
u32 native_main_02091f54(s32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 var_r4;
    s32 var_r5;
    u32 sp0;

    var_r5 = arg0;
    var_r4 = arg1;
loop_1:
    temp_r0 = native_fn_0208d9a0(&sp0, arg2);
    if (sp0 == 0) {
        return -1U;
    }
    if (sp0 > var_r4) {
        sp0 = var_r4;
    }
    native_fn_02008e0c(temp_r0, var_r5, sp0);
    native_fn_0208da30(sp0, arg2);
    var_r4 -= sp0;
    var_r5 += sp0;
    if ((s32) var_r4 <= 0) {
        return 0U;
    }
    goto loop_1;
}
