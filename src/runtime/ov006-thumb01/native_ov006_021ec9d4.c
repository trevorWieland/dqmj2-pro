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
extern u32 native_fn_ov006_021edb9c();
extern u32 native_fn_ov006_021edc78();
extern u32 native_fn_ov006_021edce4();
u32 native_ov006_021ec9d4(s32 arg0, void *arg1, u32 arg2) {
    s32 var_r0;
    s32 var_r4;
    void *var_r5;
    s32 temp_r6;

    var_r0 = arg0;
    temp_r6 = var_r0;
    var_r5 = arg1;
    var_r4 = 0;
    if (temp_r6 > 0) {
        do {
            native_fn_ov006_021edb9c(var_r5, arg2, 6);
            M2C_FIELD(var_r5, u16 *, 6) = (u16) native_fn_ov006_021edce4();
            var_r0 = (s32) native_fn_ov006_021edc78(M2C_FIELD(var_r5, u16 *, 6));
            M2C_FIELD(var_r5, u16 *, 6) = (u16) var_r0;
            var_r4 += 1;
            var_r5 += 8;
        } while (var_r4 < temp_r6);
    }
    return (u32) var_r0;
}
