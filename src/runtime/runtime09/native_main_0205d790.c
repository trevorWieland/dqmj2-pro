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
extern u32 native_fn_0205d764();
u32 native_main_0205d790(void) {
    s32 temp_r0;
    u32 var_r4;

    var_r4 = -1U;
    temp_r0 = (s32) native_fn_0205d764();
    if (temp_r0 < 0) {
        goto block_7;
    }
    if (temp_r0 != 1) {
        goto block_3;
    }
    var_r4 = 0;
    goto block_7;
block_3:
    if (temp_r0 != 2) {
        goto block_5;
    }
    var_r4 = 1;
    goto block_7;
block_5:
    if (temp_r0 != 3) {
        goto block_7;
    }
    var_r4 = 2;
block_7:
    return var_r4;
}
