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
u32 native_main_0201d914(u8 *arg0, u8 *arg1, s32 arg2) {
    s32 var_r2;
    u8 *var_r0;
    u8 *var_r1;
    u8 temp_ip;
    u8 temp_r3;

    var_r0 = arg0;
    var_r1 = arg1;
    var_r2 = arg2;
    if (var_r2 == 0) {
        goto block_5;
    }
loop_1:
    temp_ip = *var_r1;
    var_r1 += 1;
    temp_r3 = *var_r0;
    var_r0 += 1;
    if (temp_r3 == temp_ip) {
        goto block_3;
    }
    return temp_r3 - temp_ip;
block_3:
    if (temp_r3 == 0) {
        goto block_5;
    }
    var_r2 -= 1;
    if (var_r2 != 0) {
        goto loop_1;
    }
block_5:
    return 0U;
}
