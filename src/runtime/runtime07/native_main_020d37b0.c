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
extern u8 native_data_021d720e[];
u32 native_main_020d37b0(s32 arg0, s32 arg1) {
    s32 var_r3;
    u32 var_ip;
    u8 *var_lr;

    var_ip = 0;
    var_lr = native_data_021d720e;
    var_r3 = 0;
    do {
        var_r3 += 1;
        if ((arg0 == M2C_FIELD(var_lr, s16 *, 0)) && (arg1 == M2C_FIELD(var_lr, u8 *, 2))) {
            var_ip += 1;
        }
        var_lr += 6;
    } while (var_r3 < 6);
    return var_ip;
}
