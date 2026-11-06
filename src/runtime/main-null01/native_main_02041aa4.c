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
extern u32 native_fn_0205e73c();
u32 native_main_02041aa4(void *arg0) {
    s32 var_r4;
    u32 var_r5;
    void *var_r6;

    var_r6 = arg0;
    var_r5 = 0;
    if (var_r6 != NULL) {
        var_r4 = 0;
        do {
            if ((M2C_FIELD(var_r6, u16 *, 0xA) == 2) && ((s32) M2C_FIELD(var_r6, u16 *, 0xC) >= 0)) {
                native_fn_0205e73c();
                var_r5 += 1;
            }
            var_r4 += 1;
            var_r6 += 6;
        } while (var_r4 < 0x10);
    }
    return var_r5;
}
