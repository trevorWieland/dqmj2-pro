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
u32 native_main_020446cc(void *arg0, s32 arg1, s32 arg2) {
    u32 var_ip;

    var_ip = 0;
    if (arg1 < (s32) M2C_FIELD(arg0, s32 *, 4)) {
        var_ip = (arg1 * 0xC) + (s32) (arg0 + M2C_FIELD((arg0 + (arg2 * 4)), s32 *, 8));
    }
    return var_ip;
}
