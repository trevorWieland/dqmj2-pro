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
extern u32 native_arm7_fn_037fdf9c(u32, u32, u32);
u32 native_arm7_main_027eaca8(u32 arg0, u32 arg1, u32 arg2, s32 arg3) {
    u32 var_r0;

    var_r0 = native_arm7_fn_037fdf9c(arg1, arg0, 0x24U);
    if (arg3 != 0) {
        var_r0 = native_arm7_fn_037fdf9c(arg2, arg0 + 0x24, (arg3 + 1) & ~1);
    }
    return var_r0;
}
