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
extern u8 native_data_ov000_02232ae8[];
u32 native_ov000_021e5bcc(s32 arg0) {
    s32 var_r2;
    u32 var_r3;
    u8 *var_ip;

    var_r3 = 0;
    var_ip = native_data_ov000_02232ae8;
    var_r2 = 0;
loop_1:
    if ((M2C_FIELD(var_ip, u8 *, 0) != 0) && (M2C_FIELD(var_ip, u8 *, 1) == arg0)) {
        var_r3 = 1;
    } else {
        var_r2 += 1;
        var_ip += 0x20;
        if (var_r2 < 0x40) {
            goto loop_1;
        }
    }
    return var_r3;
}
