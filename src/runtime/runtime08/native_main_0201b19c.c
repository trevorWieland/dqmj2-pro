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
u32 native_main_0201b19c(s8 *arg0, s8 *arg1, s32 arg2) {
    s32 var_r2;
    s8 *var_ip;
    s8 *var_r1;
    s8 temp_r3;

    var_r1 = arg1;
    var_r2 = arg2;
    var_ip = arg0;
    if (var_r2 == 0) {
        return (u32) arg0;
    }
    do {
        temp_r3 = *var_r1;
        var_r1 += 1;
        var_r2 -= 1;
        *var_ip = temp_r3;
        var_ip += 1;
    } while (var_r2 != 0);
    return (u32) arg0;
}
