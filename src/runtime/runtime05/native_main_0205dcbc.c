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
extern u32 native_fn_0205dc88();
u32 native_main_0205dcbc(u8 *arg0, u8 *arg1) {
    u8 *var_r4;
    u8 *var_r5;
    u8 temp_r1;

    var_r5 = arg1;
    var_r4 = arg0;
    do {
        temp_r1 = *var_r5;
        var_r5 += 1;
        *var_r4 = temp_r1;
        var_r4 += 1;
    } while (native_fn_0205dc88(var_r5) != 0);
    M2C_FIELD(var_r4, u8 *, 0) = 0xE3;
    M2C_FIELD(var_r4, s8 *, 1) = 0x1B;
    return (u32) arg0;
}
