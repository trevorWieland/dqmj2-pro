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
u32 native_main_020b03a4(void **arg0, s32 arg1) {
    void *var_r0;

    var_r0 = M2C_FIELD(*arg0, void **, 0x5D4);
    if (var_r0 != NULL) {
loop_1:
        if (M2C_FIELD(var_r0, s32 *, 0x10) != arg1) {
            var_r0 = M2C_FIELD(var_r0, void **, 0x4C);
            if (var_r0 == NULL) {
                goto block_3;
            }
            goto loop_1;
        }
    } else {
block_3:
        var_r0 = NULL;
    }
    return (u32) var_r0;
}
