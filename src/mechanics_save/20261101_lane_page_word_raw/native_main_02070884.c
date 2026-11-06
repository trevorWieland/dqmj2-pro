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
#define NULL ((void *)0)
extern u32 native_fn_020624b0(u32 arg0, u32 arg1);
extern u32 native_fn_020624c0(s32 arg0);
extern u32 native_fn_02070f44(void);
u32 native_main_02070884(void) {
    s32 temp_r0;
    u32 temp_r4;
    u32 var_r5;

    temp_r4 = native_fn_02070f44();
    var_r5 = native_fn_020624c0(4U);
    temp_r0 = temp_r4 - 1;
    if ((s32) var_r5 > temp_r0) {
        var_r5 = (u32) (s8) temp_r0;
        native_fn_020624b0(4U, var_r5);
    }
    return var_r5;
}
