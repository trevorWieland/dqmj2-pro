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
extern u8 native_data_02102e2c[];
u32 native_main_0205c404(s32 arg0) {
    s32 var_r2;
    u32 var_r3;
    u8 *var_ip;

    var_r3 = 0;
    var_ip = native_data_02102e2c;
    var_r2 = 0;
loop_1:
    if (arg0 == M2C_FIELD(var_ip, s32 *, 4)) {
        var_r3 = (var_r2 * 0xAC) + (s32) native_data_02102e2c;
    } else {
        var_r2 += 1;
        var_ip += 0xAC;
        if (var_r2 < 0x20) {
            goto loop_1;
        }
    }
    return var_r3;
}
