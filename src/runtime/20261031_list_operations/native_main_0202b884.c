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
extern u8 *native_fn_0202bb88(u8 *context, u8 *previous);
u32 native_main_0202b884(u8 *arg0, u32 arg1) {
    u32 var_r0;
    u8 *var_r4;

    var_r4 = native_fn_0202bb88(arg0, NULL);
    if (var_r4 != NULL) {
        do {
        if (((u32) M2C_FIELD(var_r4, u32 *, 0x18) <= arg1) && (arg1 < (u32) M2C_FIELD(var_r4, u32 *, 0x1C))) {
            var_r0 = native_main_0202b884(var_r4 + 0xC, arg1);
            if (var_r0 == 0) {
                var_r0 = (u32) var_r4;
            }
            return var_r0;
        }
        var_r4 = native_fn_0202bb88(arg0, var_r4);
        } while (var_r4 != NULL);
    }
    return 0U;
}
