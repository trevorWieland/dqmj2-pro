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
extern u32 native_fn_020d3540();
extern u8 native_data_020e32f4[];
u32 native_main_020d3a04(void) {
    u32 var_r5;
    s32 var_r6;
    u32 var_r7;

    var_r5 = 0;
    var_r7 = native_fn_02062b00();
    var_r6 = 0;
    do {
        if ((M2C_FIELD(var_r7, s32 *, 0x14) != 0) && (M2C_FIELD(native_data_020e32f4, s32 *, 4) & native_fn_020d3540(M2C_FIELD(var_r7, s16 *, 0x18)))) {
            var_r5 += 1;
        }
        var_r6 += 1;
        var_r7 += 0x84;
    } while (var_r6 < 0x64);
    return var_r5;
}
