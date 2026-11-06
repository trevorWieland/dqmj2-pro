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
u32 native_main_02021258(u16 *arg0) {
    u16 *var_r0;
    u16 temp_r1;
    u32 var_r2;

    var_r0 = arg0;
    var_r2 = -1U;
    do {
        temp_r1 = *var_r0;
        var_r0 += 0x1;
        var_r2 += 1;
    } while (temp_r1 != 0);
    return var_r2;
}
