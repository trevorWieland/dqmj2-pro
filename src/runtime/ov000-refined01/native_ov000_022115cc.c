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
extern u8 native_data_ov000_02240ddc[];
u32 native_ov000_022115cc(s32 arg0, s32 arg1) {
    s32 var_r3;
    s32 var_ip;
    u8 *var_lr;

    var_lr = native_data_ov000_02240ddc;
    var_ip = -1;
    var_r3 = 0;
loop_1:
    if ((arg0 == M2C_FIELD(var_lr, s16 *, 0)) && (arg1 == M2C_FIELD(var_lr, s16 *, 2))) {
        var_ip = var_r3;
    } else {
        var_r3 += 1;
        var_lr += 0x60;
        if (var_r3 < 5) {
            goto loop_1;
        }
    }
    return (u32) var_ip;
}
