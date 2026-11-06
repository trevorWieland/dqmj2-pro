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
extern u32 native_fn_02008d78();
extern u32 native_fn_02008e0c();
u32 native_main_02015bf8(void *arg0, u32 arg1, u32 arg2, s32 arg3) {
    u32 temp_ip;
    u32 temp_r1;
    u32 var_lr;
    u32 var_r2;

    var_r2 = arg2;
    var_lr = arg1;
    temp_ip = M2C_FIELD(arg0, u32 *, 0);
    if (var_lr < 0x4000U) {
        var_lr = 0x4000;
    }
    if (var_r2 > 0x8000U) {
        var_r2 = 0x8000;
    }
    temp_r1 = temp_ip + M2C_FIELD(arg0, s32 *, 0xC);
    if (var_lr < temp_ip) {
        var_lr = temp_ip;
    }
    if (var_r2 > temp_r1) {
        var_r2 = temp_r1;
    }
    if (var_lr >= var_r2) {
        return (u32) arg0;
    }
    if (arg3 != 0) {
        return native_fn_02008d78(M2C_FIELD(arg0, s32 *, 8) + var_lr, 0, var_r2 - var_lr);
    }
    return native_fn_02008e0c(M2C_FIELD(arg0, s32 *, 4) + var_lr, M2C_FIELD(arg0, s32 *, 8) + var_lr, var_r2 - var_lr);
}
