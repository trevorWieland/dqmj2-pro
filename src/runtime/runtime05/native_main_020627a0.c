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
extern u32 native_fn_02062828();
extern u8 native_data_021bd674[];
u32 native_main_020627a0(s32 arg0) {
    s32 var_r2;
    u32 var_r3;
    u8 *var_ip;

    var_r3 = 0;
    var_ip = native_data_021bd674;
    var_r2 = 0;
loop_1:
    if (M2C_FIELD(var_ip, s32 *, 0x14) == arg0) {
        M2C_FIELD(var_ip, s32 *, 0x14) = 0;
        native_fn_02062828();
        var_r3 = 1;
    } else {
        var_r2 += 1;
        var_ip += 0x84;
        if (var_r2 < 0x64) {
            goto loop_1;
        }
    }
    return var_r3;
}
