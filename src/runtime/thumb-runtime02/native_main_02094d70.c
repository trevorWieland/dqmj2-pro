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
extern u32 native_fn_020946ec();
extern u32 native_fn_0209477c();
extern u32 native_fn_02094d9c();
extern u32 native_fn_02094e68();
u32 native_main_02094d70(void) {
    u32 var_r4;

    var_r4 = native_fn_0209477c();
    native_fn_020946ec(0x10);
    switch (var_r4) {
    case 7:
        var_r4 = native_fn_02094d9c();
        break;
    case 8:
        var_r4 = native_fn_02094e68();
        break;
    }
    return var_r4;
}
