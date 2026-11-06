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
extern u32 native_fn_0202a634();
u32 native_main_02049618(void *arg0) {
    s8 *var_r1;
    u32 temp_r0;
    u32 var_r3;
    u8 *var_ip;
    u8 temp_r2;

    temp_r0 = native_fn_0202a634();
    temp_r2 = M2C_FIELD(arg0, u8 *, 0x14);
    var_r3 = 0;
    if (temp_r2 == 0) {
        var_r1 = arg0 + 8;
    } else {
        var_r1 = arg0 + 0xA;
    }
    if (temp_r2 == 0) {
        var_ip = arg0 + 9;
    } else {
        var_ip = arg0 + 0xB;
    }
    if (M2C_FIELD(temp_r0, u16 *, 6) & 0x80) {
        *var_r1 += 1;
        if ((s32) *var_r1 >= (s32) *var_ip) {
            *var_r1 = 0;
        }
        var_r3 = 1;
    }
    if (M2C_FIELD(temp_r0, u16 *, 6) & 0x40) {
        var_r3 = -1U;
        *var_r1 -= 1;
        if ((s32) *var_r1 < 0) {
            *var_r1 = *var_ip - 1;
        }
    }
    return var_r3;
}
