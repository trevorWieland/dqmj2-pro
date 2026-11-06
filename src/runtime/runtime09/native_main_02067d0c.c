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
extern u8 native_data_021c3708[];
extern u8 native_data_021c37f0[];
u32 native_main_02067d0c(s32 arg0) {
    s32 var_r2;
    u8 *var_r3;

    var_r2 = 0;
    if ((s32) M2C_FIELD(native_data_021c3708, s32 *, 0xC) <= 0) {
        goto block_5;
    }
    var_r3 = native_data_021c37f0;
loop_2:
    if (*var_r3 != arg0) {
        goto block_4;
    }
    return 1U;
block_4:
    var_r2 += 1;
    var_r3 += 1;
    if (var_r2 < (s32) M2C_FIELD(native_data_021c3708, s32 *, 0xC)) {
        goto loop_2;
    }
block_5:
    return 0U;
}
