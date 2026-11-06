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
extern u32 native_fn_0200e77c();
u32 native_main_0200e8dc(s32 arg0, s32 arg1, u32 arg2, s32 arg3) {
    s32 var_r2;

    var_r2 = 0;
    if (arg0 != 0) {
        goto block_6;
    }
    if (arg1 != 1) {
        goto block_3;
    }
    var_r2 = 6;
block_3:
    if (arg1 != 0) {
        goto block_5;
    }
    var_r2 = 7;
block_5:
    goto block_17;
block_6:
    if (arg0 != 1) {
        goto block_12;
    }
    if (arg1 != 1) {
        goto block_9;
    }
    var_r2 = 4;
block_9:
    if (arg1 != 0) {
        goto block_11;
    }
    var_r2 = 5;
block_11:
    goto block_17;
block_12:
    if (arg0 != 2) {
        goto block_17;
    }
    if (arg1 != 1) {
        goto block_15;
    }
    var_r2 = 8;
block_15:
    if (arg1 != 0) {
        goto block_17;
    }
    var_r2 = 9;
block_17:
    if (var_r2 != 0) {
        goto block_19;
    }
    return 0xFFFFU;
block_19:
    return native_fn_0200e77c(var_r2, 0, 0, arg2, arg3);
}
