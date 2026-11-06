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
extern u32 native_fn_020061ac();
extern u32 native_fn_0201d69c();
extern u32 native_fn_02098adc();
extern u8 native_data_020deec0[];
u32 native_main_02098a0c(s32 arg0, u32 arg1) {
    s32 temp_r0;
    u32 temp_r0_2;
    s32 var_r2;
    void *temp_r5;

    temp_r5 = arg0 + 0x19F8;
    temp_r0 = (s32) native_fn_0201d69c(arg1);
    var_r2 = M2C_FIELD(temp_r5, s32 *, 8) - M2C_FIELD(temp_r5, s32 *, 4);
    if (temp_r0 > var_r2) {
        if (native_fn_02098adc(arg0, temp_r5, (temp_r0 - var_r2) + 1) == 0) {
            return 1U;
        }
        var_r2 = M2C_FIELD(temp_r5, s32 *, 8) - M2C_FIELD(temp_r5, s32 *, 4);
        goto block_4;
    }
block_4:
    temp_r0_2 = native_fn_020061ac(M2C_FIELD(temp_r5, s32 *, 4), var_r2, native_data_020deec0, arg1);
    if (temp_r0_2 != temp_r0) {
        return 1U;
    }
    M2C_FIELD(temp_r5, s32 *, 4) = (s32) (M2C_FIELD(temp_r5, s32 *, 4) + temp_r0_2);
    return 0U;
}
