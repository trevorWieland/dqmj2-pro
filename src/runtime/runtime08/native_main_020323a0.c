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
extern u32 native_fn_02032684();
u32 native_main_020323a0(u32 arg0, void *arg1, u32 arg2) {
    s32 var_ip;
    u16 temp_r1;
    void *temp_r0;

    temp_r0 = M2C_FIELD(arg1, void **, 8);
    var_ip = M2C_FIELD(arg1, s32 *, 0);
    temp_r1 = M2C_FIELD(temp_r0, u16 *, 4);
    if (var_ip >= (s32) (temp_r1 << 0xC)) {
        var_ip = (temp_r1 << 0xC) - 1;
    } else if (var_ip < 0) {
        var_ip = 0;
    }
    return native_fn_02032684(temp_r0, arg2, var_ip, arg0);
}
