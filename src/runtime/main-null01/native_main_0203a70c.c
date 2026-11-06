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
extern u32 native_fn_02007ff4();
extern u32 native_fn_02008008();
extern u32 native_fn_0202bb28();
extern u32 native_fn_0202bb88();
extern u32 native_fn_0203a80c();
u32 native_main_0203a70c(u32 arg0, s32 arg1) {
    u32 temp_r4;
    u8 *var_r5;
    u8 *temp_r6;

    temp_r4 = native_fn_02007ff4();
    var_r5 = native_fn_0202bb88(arg0, NULL);
    if (var_r5 != NULL) {
        do {
            temp_r6 = native_fn_0202bb88(arg0, var_r5);
            if (M2C_FIELD(var_r5, s32 *, 8) == arg1) {
                native_fn_0202bb28(arg0, var_r5);
                native_fn_0203a80c(var_r5);
            }
            var_r5 = temp_r6;
        } while (temp_r6 != NULL);
    }
    return native_fn_02008008(temp_r4);
}
