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
extern u32 native_fn_020af1c4();
extern u32 native_fn_020afa1c();
u32 native_main_020b0464(u32 arg0, void *arg1) {
    void *spC;
    u32 var_r0;

    var_r0 = native_fn_020afa1c(arg0, 2, 0, &spC, 0, 0, 0);
    if (var_r0 == 0) {
        var_r0 = native_fn_020af1c4(arg0, M2C_FIELD(arg1, s32 *, 0x10), M2C_FIELD(spC, s32 *, 0x18));
        if (var_r0 == 0) {
            M2C_FIELD(arg1, s32 *, 0) = 0x65;
            var_r0 = 0;
        }
    }
    return var_r0;
}
