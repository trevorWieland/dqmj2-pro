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
u32 native_main_02019da8(s8 *arg0, s8 *arg1) {
    s8 *var_r0;
    s8 *var_r1;
    s8 temp_r2;
    s8 temp_r3;

    var_r0 = arg0;
    var_r1 = arg1;
    goto loop_2;
block_1:
    var_r0 += 1;
    var_r1 += 1;
loop_2:
    temp_r3 = *var_r1;
    temp_r2 = *var_r0;
    if (temp_r2 != temp_r3) {
        goto block_4;
    }
    if (temp_r2 != 0) {
        goto block_1;
    }
block_4:
    return temp_r2 - temp_r3;
}
