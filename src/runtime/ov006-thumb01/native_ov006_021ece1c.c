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
extern u32 native_fn_ov006_021edb7c();
extern u8 native_data_ov006_0221a8ac[];
u32 native_ov006_021ece1c(s32 arg0, u32 arg1) {
    s32 var_r3;
    u32 var_r4;
    s32 var_r5;
    u8 *var_r6;

    var_r4 = 0;
    var_r6 = native_data_ov006_0221a8ac;
    var_r5 = 0;
    var_r3 = 0;
loop_1:
    if (*var_r6 != 0) {
        var_r5 = 1;
    } else {
        var_r3 += 1;
        var_r6 += 1;
        if (var_r3 < 6) {
            goto loop_1;
        }
    }
    if (var_r5 != 0) {
        if (native_fn_ov006_021edb7c(native_data_ov006_0221a8ac, arg1, 6) != 0) {
            var_r4 = 1;
        }
    } else if (arg0 != 0x1000) {
        var_r4 = 2;
    }
    return var_r4;
}
