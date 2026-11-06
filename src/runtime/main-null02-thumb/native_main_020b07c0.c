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
extern u32 native_fn_020a929c();
u32 native_main_020b07c0(void *arg0, void *arg1) {
    void *var_r0;
    void *temp_r2;
    void *temp_r2_2;
    void *var_r3;

    var_r0 = arg0;
    if ((var_r0 != NULL) && (arg1 != NULL) && (M2C_FIELD(var_r0, void **, 0x40) != NULL)) {
        var_r3 = M2C_FIELD(var_r0, void **, 0x44);
        if ((var_r3 == M2C_FIELD(var_r0, void **, 0x48)) && (var_r3 == arg1)) {
            temp_r2 = M2C_FIELD(arg1, void **, 0xC);
            M2C_FIELD(var_r0, void **, 0x48) = temp_r2;
            M2C_FIELD(var_r0, void **, 0x44) = temp_r2;
            M2C_FIELD(var_r0, void **, 0x40) = temp_r2;
            goto block_12;
        }
        if (var_r3 == arg1) {
            temp_r2_2 = M2C_FIELD(var_r3, void **, 0xC);
            M2C_FIELD(var_r0, void **, 0x44) = temp_r2_2;
            M2C_FIELD(var_r0, void **, 0x40) = temp_r2_2;
            goto block_12;
        }
        var_r0 = M2C_FIELD(var_r3, void **, 0xC);
        if (var_r0 != arg1) {
loop_9:
            if (var_r0 != NULL) {
                var_r3 = var_r0;
                var_r0 = M2C_FIELD(var_r0, void **, 0xC);
                if (var_r0 == arg1) {
                    goto block_11;
                }
                goto loop_9;
            }
        } else {
block_11:
            M2C_FIELD(var_r3, void **, 0xC) = (void *) M2C_FIELD(arg1, void **, 0xC);
block_12:
            var_r0 = (void *) native_fn_020a929c(arg1);
        }
    }
    return (u32) var_r0;
}
