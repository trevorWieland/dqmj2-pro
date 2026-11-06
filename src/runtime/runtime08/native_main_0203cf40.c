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
extern u32 native_fn_0203cc4c();
extern u32 native_fn_0203cebc();
extern u32 native_fn_0203cf9c();
u32 native_main_0203cf40(u32 arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 var_r5;

    var_r5 = 0;
    temp_r0 = native_fn_0203cebc(arg0, arg1, arg2, 1);
    if (temp_r0 != 0) {
        var_r5 = native_fn_0203cc4c(temp_r0, arg2);
        native_fn_0203cf9c(arg2, temp_r0);
    }
    return var_r5;
}
