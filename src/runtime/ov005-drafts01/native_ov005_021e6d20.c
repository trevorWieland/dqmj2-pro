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
extern u32 native_fn_02044dc4();
u32 native_ov005_021e6d20(void *arg0) {
    s16 temp_r0;
    s32 var_r4;
    void *var_r5;

    var_r5 = arg0;
    var_r4 = 0;
loop_1:
    temp_r0 = M2C_FIELD(var_r5, s16 *, 0x18);
    if (((s32) temp_r0 > 0) && (native_fn_02044dc4(temp_r0, M2C_FIELD(var_r5, u8 *, 0x1A)) <= 6U)) {
        return 1U;
    }
    var_r4 += 1;
    var_r5 += 0x84;
    if (var_r4 >= 3) {
        return 0U;
    }
    goto loop_1;
}
