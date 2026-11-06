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
extern u32 native_arm7_data_04805f60;
extern u32 native_arm7_data_0380fff4;
u32 native_arm7_main_027eac0c(u32 arg0, u32 arg1, s32 arg2) {
    u32 temp_r2;
    u32 var_r0;
    u32 var_r4;
    u32 var_r7;

    temp_r2 = (arg2 + 1) & ~1;
    if ((u32) (arg1 + temp_r2) > (u32) (u32) &native_arm7_data_04805f60) {
        var_r4 = (u32) &native_arm7_data_04805f60 - arg1;
        var_r7 = temp_r2 - var_r4;
    } else {
        var_r4 = temp_r2;
        var_r7 = 0;
    }
    var_r0 = native_arm7_fn_037fdf9c(arg1, arg0, var_r4);
    if (var_r7 != 0) {
        var_r0 = native_arm7_fn_037fdf9c((arg1 + var_r4) - M2C_FIELD(native_arm7_data_0380fff4, u16 *, 0x3DE), arg0 + var_r4, var_r7);
    }
    return var_r0;
}
