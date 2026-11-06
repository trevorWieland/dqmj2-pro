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
extern u32 native_fn_020410a8();
extern u8 native_data_020f6114[];
u32 native_main_02041d78(void) {
    u32 var_r4;
    s32 var_r5;
    u8 *var_r6;

    var_r4 = 0;
    var_r6 = native_data_020f6114;
    var_r5 = 0;
    do {
        if (M2C_FIELD(var_r6, u8 *, 0x39) != 0) {
            var_r4 |= native_fn_020410a8(var_r6);
        }
        var_r5 += 1;
        var_r6 += 0x58;
    } while (var_r5 < 3);
    return var_r4;
}
