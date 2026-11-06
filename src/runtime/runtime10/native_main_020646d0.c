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
extern u32 native_fn_02062a10();
extern u32 native_fn_020633b0();
u32 native_main_020646d0(s32 arg0) {
    u32 temp_r0;
    u32 temp_r0_2;
    u32 temp_r4;
    s32 var_r5;
    s32 var_r5_2;

    temp_r4 = native_fn_020633b0();
    var_r5 = 0;
loop_1:
    temp_r0 = native_fn_02062a10(M2C_FIELD((temp_r4 + (var_r5 * 4)), s32 *, 0x1C));
    if ((temp_r0 != 0) && (M2C_FIELD(temp_r0, u8 *, 0x1D) != 0)) {
        return 0U;
    }
    var_r5 += 1;
    if (var_r5 >= 3) {
        if (arg0 == 0) {
            return 1U;
        }
        var_r5_2 = 0;
loop_8:
        temp_r0_2 = native_fn_02062a10(M2C_FIELD((temp_r4 + (var_r5_2 * 4)), s32 *, 0x28));
        if ((temp_r0_2 != 0) && (M2C_FIELD(temp_r0_2, u8 *, 0x1D) != 0)) {
            return 0U;
        }
        var_r5_2 += 1;
        if (var_r5_2 >= 3) {
            return 1U;
        }
        goto loop_8;
    }
    goto loop_1;
}
