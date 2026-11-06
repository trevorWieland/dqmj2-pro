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
extern u8 native_data_020dc96c[];
u32 native_main_020cf5e8(u32 arg0, s32 arg1) {
    u32 var_r3;
    u8 *var_ip;

    var_ip = native_data_020dc96c;
    var_r3 = 0;
loop_1:
    if ((M2C_FIELD(var_ip, s16 *, 2) == arg0) && (M2C_FIELD(var_ip, u8 *, 4) == arg1)) {
        return (u32) M2C_FIELD(var_ip, s16 *, 0);
    }
    var_r3 += 1;
    var_ip += 6;
    if (var_r3 >= 0xEU) {
        return arg0;
    }
    goto loop_1;
}
