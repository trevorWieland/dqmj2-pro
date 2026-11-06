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
extern u32 native_fn_0203c738();
u32 native_main_0203caa4(u32 arg0, s32 arg1) {
    s32 var_r2;

    var_r2 = arg1;
    if (var_r2 == 0x41) {
        var_r2 = 0x20;
    }
    return native_fn_0203c738(0, arg0, var_r2, 5);
}
