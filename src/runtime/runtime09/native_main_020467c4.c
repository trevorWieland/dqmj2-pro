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
u32 native_main_020467c4(s32 arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4, u8 arg5, s32 arg6) {
    u32 var_lr;

    var_lr = 0x10;
    if (arg5 != arg1) {
        goto block_7;
    }
    if (arg4 != arg0) {
        goto block_3;
    }
    var_lr = 0;
    goto block_27;
block_3:
    if (arg4 != arg2) {
        goto block_5;
    }
    var_lr = 2;
    goto block_6;
block_5:
    var_lr = 1;
block_6:
    goto block_27;
block_7:
    if (arg5 != arg3) {
        goto block_14;
    }
    if (arg4 != arg0) {
        goto block_10;
    }
    var_lr = 5;
    goto block_27;
block_10:
    if (arg4 != arg2) {
        goto block_12;
    }
    var_lr = 7;
    goto block_13;
block_12:
    var_lr = 6;
block_13:
    goto block_27;
block_14:
    if ((arg5 - arg1) != 3) {
        goto block_17;
    }
    if (arg6 != 1) {
        goto block_17;
    }
    goto block_22;
block_17:
    if (arg4 != arg0) {
        goto block_19;
    }
    var_lr = 3;
    goto block_27;
block_19:
    if (arg4 != arg2) {
        goto block_21;
    }
    var_lr = 4;
block_21:
    goto block_27;
block_22:
    if (arg4 != arg0) {
        goto block_24;
    }
    var_lr = 8;
    goto block_27;
block_24:
    if (arg4 != arg2) {
        goto block_26;
    }
    var_lr = 0xA;
    goto block_27;
block_26:
    var_lr = 9;
block_27:
    return var_lr;
}
