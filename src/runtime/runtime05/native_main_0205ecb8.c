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
extern u32 native_fn_0205f304();
u32 native_main_0205ecb8(s32 arg0) {
    s32 temp_r0;
    s32 var_r5;
    u32 var_r6;

    var_r6 = 0;
    var_r5 = 0;
    do {
        temp_r0 = (s32) native_fn_0205f304(var_r5);
        if ((temp_r0 > 0) && (arg0 == temp_r0)) {
            var_r6 = 1;
        }
        var_r5 += 1;
    } while (var_r5 < 0x10);
    return var_r6;
}
