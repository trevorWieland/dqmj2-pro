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
extern u32 native_fn_0207b674();
u32 native_main_0207d144(u32 arg0, u32 arg1) {
    u32 var_r5;

    var_r5 = arg0;
    if ((s32) native_fn_0207b674(0x79) <= 0) {
        goto block_2;
    }
    var_r5 *= 2;
    goto block_6;
block_2:
    if ((s32) native_fn_0207b674(2, arg1) <= 0) {
        goto block_4;
    }
    var_r5 *= 3;
    goto block_6;
block_4:
    if ((s32) native_fn_0207b674(0x7A, arg1) <= 0) {
        goto block_6;
    }
    var_r5 *= 4;
block_6:
    return var_r5;
}
