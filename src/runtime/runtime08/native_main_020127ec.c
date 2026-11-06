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
extern u32 native_fn_02011834();
extern u32 native_fn_020118a4();
extern u32 native_fn_020119ec();
u32 native_main_020127ec(u32 arg0) {
    u32 temp_r0;
    u32 var_r0;

    temp_r0 = native_fn_020119ec();
    if (temp_r0 != 0) {
        return temp_r0;
    }
    native_fn_02011834(1, arg0);
    var_r0 = native_fn_020118a4(1, 0);
    if (var_r0 == 0) {
        var_r0 = 2;
    }
    return var_r0;
}
