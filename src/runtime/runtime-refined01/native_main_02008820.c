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
extern u32 native_fn_02008430();
u32 native_main_02008820(u32 arg0, s32 arg1) {
    s32 var_r4;
    u32 *var_r5;
    u32 temp_r7;
    u32 var_r0;

    var_r0 = arg0;
    var_r5 = (u32 *)0x040000B8;
    temp_r7 = var_r0;
    var_r4 = 0;
    do {
        if (var_r4 != temp_r7) {
            var_r0 = *var_r5;
            if ((var_r0 & 0x80000000) && (var_r0 &= 0x38000000, (var_r0 != arg1))) {
                if ((var_r0 == 0x08000000) && (arg1 == 0x10000000)) {

                } else if ((var_r0 == 0x10000000) && (arg1 == 0x08000000)) {

                } else if ((var_r0 != 0x18000000) && (var_r0 != 0x20000000) && (var_r0 != 0x28000000) && (var_r0 != 0x30000000) && (var_r0 != 0x38000000) && (var_r0 != 0x08000000) && (var_r0 != 0x10000000)) {

                } else {
                    var_r0 = native_fn_02008430();
                }
            }
        }
        var_r4 += 1;
        var_r5 += 0x3;
    } while (var_r4 < 3);
    return var_r0;
}
