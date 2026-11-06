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
extern u32 native_fn_02062b00();
extern u32 native_fn_02063fb8();
u32 native_main_02064000(void) {
    s32 var_r4;
    u32 var_r0;
    u32 var_r5;

    var_r5 = native_fn_02062b00();
    var_r4 = 0;
    do {
        var_r0 = M2C_FIELD(var_r5, u32 *, 0x14);
        if (var_r0 != 0) {
            var_r0 = native_fn_02063fb8((void *) var_r5);
        }
        var_r4 += 1;
        var_r5 += 0x84;
    } while (var_r4 < 0x64);
    return var_r0;
}
