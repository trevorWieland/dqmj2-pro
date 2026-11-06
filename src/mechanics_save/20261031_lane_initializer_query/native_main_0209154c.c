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
extern u32 native_fn_02091518(u32 bytes,s32 count,s32 width,u32 wanted);
extern u8 native_data_020de830[];
u32 native_main_0209154c(u32 arg0, s32 arg1, s32 arg2) {
    u32 var_r4;
    u8 *var_r5;
    s32 sp0;

    var_r5 = native_data_020de830;
    sp0 = arg2;
    var_r4 = 0;
loop_1:
    if (native_fn_02091518(arg0, arg1, sp0, *(u16 *)var_r5) != 0) {
        return (u32) *(u16 *)(native_data_020de830 + (var_r4 * 2));
    }
    var_r4 += 1;
    var_r5 += 2;
    if (var_r4 >= 2U) {
        return 0U;
    }
    goto loop_1;
}
