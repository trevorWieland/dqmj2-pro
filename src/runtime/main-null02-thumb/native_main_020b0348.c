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
extern u32 native_fn_020a8e7c();
extern u32 native_fn_020a9d1c();
extern u32 native_fn_020b0250();
extern u32 native_fn_020b02cc();
u32 native_main_020b0348(void **arg0) {
    u32 temp_r0;
    void *temp_r4;
    void *var_r4;
    void *temp_r6;

    temp_r4 = *arg0;
    native_fn_020a9d1c();
    var_r4 = M2C_FIELD(temp_r4, void **, 0x5D4);
    if (var_r4 != NULL) {
        do {
            temp_r6 = M2C_FIELD(var_r4, void **, 0x4C);
            if (M2C_FIELD(var_r4, s32 *, 0) == 0x6A) {
                native_fn_020b02cc(arg0, var_r4);
            } else {
                temp_r0 = native_fn_020b0250(arg0, var_r4);
                if ((M2C_FIELD(var_r4, s32 *, 0) == 0x6A) || (temp_r0 != 0) || ((s32) native_fn_020a8e7c(0) > (s32) M2C_FIELD(var_r4, s32 *, 0x14))) {
                    native_fn_020b02cc(arg0, var_r4);
                }
            }
            var_r4 = temp_r6;
        } while (temp_r6 != NULL);
    }
    return 0U;
}
