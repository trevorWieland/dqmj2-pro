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
extern u32 native_fn_02008c58();
extern u32 native_fn_0201d444();
extern u32 native_fn_0202bd74();
extern u8 native_data_020edd44[];
u32 native_main_02028d50(void *arg0, u32 arg1) {
    s32 temp_r0;
    s32 var_r0_2;
    u32 var_r0;

    native_fn_02008c58(0, native_data_020edd44, 0x10);
    native_fn_0201d444(native_data_020edd44, arg1);
    temp_r0 = M2C_FIELD(arg0, s32 *, 0x10);
    if (temp_r0 != 0) {
        var_r0_2 = temp_r0 + 0x40;
    } else {
        var_r0_2 = 0;
    }
    if (var_r0_2 == 0) {
        var_r0 = -1U;
    } else {
        var_r0 = native_fn_0202bd74(var_r0_2, native_data_020edd44);
    }
    if ((s32) var_r0 < 0) {
        var_r0 = -1U;
    }
    return var_r0;
}
