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
#define NULL ((void *)0)
extern u32 native_fn_020c3780(u32 count);
extern u8 native_data_021d4cf4[];
u32 native_main_020c3724(u32 *arg0) {
    u8 var_ip;
    u8 var_lr;

    var_lr = 0;
    var_ip = 0;
    do {
        M2C_FIELD((native_data_021d4cf4 + (var_ip * 4)), s32 *, 0x44) = (s32) arg0[var_ip];
        if (arg0[var_ip] != 0) {
            var_lr += 1;
        }
        var_ip += 1;
    } while ((u32) var_ip < 3U);
    return native_fn_020c3780(var_lr);
}
