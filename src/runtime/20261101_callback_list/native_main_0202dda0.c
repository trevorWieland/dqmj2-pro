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
u32 native_main_0202dda0(u32 arg0, void *arg1, u32 arg2) {
    u32 (*temp_r3)(u32, void *, u8);
    u16 temp_r2;
    u32 var_r0;
    void *var_r5;

    var_r5 = arg1;
    var_r0 = 0;
    if (var_r5 == NULL) {
        return 0U;
    }
    do {
        if (arg2 < (u32) M2C_FIELD(var_r5, u8 *, 0x19)) {
            temp_r2 = M2C_FIELD((var_r5 + (arg2 * 2)), u16 *, 0x1A);
            if ((temp_r2 & 0x100) && (temp_r3 = M2C_FIELD(var_r5, u32 (**)(u32, void *, u8), 0xC), (temp_r3 != NULL))) {
                temp_r3(arg0, var_r5, (u8) temp_r2);
                var_r0 = 1;
            }
        }
        var_r5 = M2C_FIELD(var_r5, void **, 0x10);
    } while (var_r5 != NULL);
    return var_r0;
}
