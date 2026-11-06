#define NULL ((void *)0)
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
extern u32 native_fn_0200e800();
u32 native_main_0200eaf4(s32 *arg0, s32 *arg1) {
    u32 temp_r0;
    s32 var_r1;
    s32 var_r1_2;
    u16 sp0;

    temp_r0 = native_fn_0200e800(0xF, 1, &sp0);
    if (temp_r0 != 0) {
        return temp_r0;
    }
    if (arg0 != NULL) {
        if (sp0 & 8) {
            var_r1 = 1;
        } else {
            var_r1 = 0;
        }
        *arg0 = var_r1;
    }
    if (arg1 == NULL) {
        return temp_r0;
    }
    if (sp0 & 4) {
        var_r1_2 = 1;
    } else {
        var_r1_2 = 0;
    }
    *arg1 = var_r1_2;
    return temp_r0;
}
