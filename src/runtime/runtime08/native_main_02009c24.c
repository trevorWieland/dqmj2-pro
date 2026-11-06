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
extern u8 native_data_020e5260[];
u32 native_main_02009c24(void) {
    s32 var_r1;
    u8 *var_r2;

    var_r1 = 0;
    var_r2 = native_data_020e5260;
    do {
        M2C_FIELD(var_r2, s32 *, 0) = 0;
        M2C_FIELD(var_r2, s32 *, 4) = 0;
        var_r1 += 1;
        M2C_FIELD(var_r2, s8 *, 8) = 0;
        var_r2 += 0xC;
    } while (var_r1 < 8);
    return 0U;
}
