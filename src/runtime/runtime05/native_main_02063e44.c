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
u32 native_main_02063e44(s32 arg0) {
    s32 var_r2;
    u32 var_r3;
    u8 temp_r1;

    if (arg0 != 0) {
        var_r2 = 0;
        var_r3 = 0;
        do {
            temp_r1 = M2C_FIELD((arg0 + (var_r2 * 2)), u8 *, 0x7A);
            var_r2 += 1;
            if (temp_r1 != 0) {
                var_r3 += 1;
            }
        } while (var_r2 < 5);
    } else {
        var_r3 = -1U;
    }
    return var_r3;
}
