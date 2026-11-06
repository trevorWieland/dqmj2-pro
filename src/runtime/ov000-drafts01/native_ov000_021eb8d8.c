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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_020633b0();
u32 native_ov000_021eb8d8(s32 arg0, s32 arg1) {
    s32 *var_r2;
    s32 *var_r3;
    s32 temp_r0_2;
    s32 temp_r1;
    s32 var_ip;
    s32 var_r4;
    u32 temp_r0;

    var_r4 = arg0;
    temp_r0 = native_fn_020633b0();
    if (arg1 != 0) {
        var_r2 = temp_r0 + 0x14;
    } else {
        var_r2 = temp_r0 + 0x18;
    }
    if (arg1 != 0) {
        var_r3 = temp_r0 + 0x18;
    } else {
        var_r3 = temp_r0 + 0x14;
    }
    temp_r0_2 = *var_r2;
    if (arg1 != 0) {
        var_ip = 0x98967F;
    } else {
        var_ip = 0xF423F;
    }
    temp_r1 = *var_r3;
    if (temp_r0_2 < var_r4) {
        var_r4 = temp_r0_2;
    }
    if ((s32) (temp_r1 + var_r4) > var_ip) {
        var_r4 = var_ip - temp_r1;
    }
    *var_r2 -= var_r4;
    *var_r3 += var_r4;
    return (u32) var_r4;
}
