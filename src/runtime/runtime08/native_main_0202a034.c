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
extern u32 native_fn_02029f98();
extern u8 native_data_020edd64[];
u32 native_main_0202a034(u32 arg0) {
    s32 temp_r4;
    s32 temp_r5;
    s32 var_r6;
    u32 var_r7;
    u8 *var_r8;

    var_r7 = 0;
    var_r8 = native_data_020edd64;
    var_r6 = 0;
loop_1:
    if ((M2C_FIELD(var_r8, s32 *, 0) != 0) && (temp_r5 = M2C_FIELD(var_r8, s32 *, 4), temp_r4 = M2C_FIELD(var_r8, s32 *, 8), (native_fn_02029f98(temp_r5 + temp_r4, arg0) != 0))) {
        var_r7 = temp_r5 + temp_r4;
    } else {
        var_r6 += 1;
        var_r8 += 0x14;
        if (var_r6 < 0x11) {
            goto loop_1;
        }
    }
    return var_r7;
}
