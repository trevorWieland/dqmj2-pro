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
extern u32 native_fn_0207b3a0(u32 arg0);
u32 native_main_0207b6ac(s32 arg0) {
    u32 var_r4;
    u8 var_r5;

    var_r5 = 0;
    var_r4 = 0;
loop_1:
    if (arg0 == (u8) native_fn_0207b3a0(var_r4)) {
        var_r5 = (u8) var_r4;
    } else {
        var_r4 += 1;
        if ((s32) var_r4 < 0x100) {
            goto loop_1;
        }
    }
    return (u32) var_r5;
}
