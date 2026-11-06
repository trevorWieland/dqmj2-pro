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
u32 native_main_0202eb4c(void **arg0, void *arg1) {
    void *var_r2;
    void *var_r3;

    var_r3 = *arg0;
    if (var_r3 == NULL) {
        return 0U;
    }
    if (var_r3 == arg1) {
        *arg0 = M2C_FIELD(var_r3, void **, 0x10);
        M2C_FIELD(arg1, s32 *, 0x10) = 0;
        return 1U;
    }
    var_r2 = M2C_FIELD(var_r3, void **, 0x10);
    if (var_r2 != NULL) {
        do {
        if (var_r2 == arg1) {
            M2C_FIELD(var_r3, void **, 0x10) = (void *) M2C_FIELD(var_r2, void **, 0x10);
            M2C_FIELD(var_r2, void **, 0x10) = NULL;
            return 1U;
        }
        var_r3 = var_r2;
        var_r2 = M2C_FIELD(var_r2, void **, 0x10);
        } while (var_r2 != NULL);
    }
    return 0U;
}
