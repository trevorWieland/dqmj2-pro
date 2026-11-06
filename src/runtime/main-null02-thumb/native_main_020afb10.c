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
u32 native_main_020afb10(void **arg0, void **arg1, s32 arg2) {
    void *var_r3;

    var_r3 = M2C_FIELD(*arg0, void **, 0x5C4);
    if (var_r3 != NULL) {
loop_1:
        if (M2C_FIELD(var_r3, s32 *, 0x18) == arg2) {
            if (arg1 != NULL) {
                *arg1 = var_r3;
            }
            return 1U;
        }
        var_r3 = M2C_FIELD(var_r3, void **, 0x20);
        if (var_r3 == NULL) {
            goto block_6;
        }
        goto loop_1;
    }
block_6:
    if (arg1 != NULL) {
        *arg1 = NULL;
    }
    return 0U;
}
