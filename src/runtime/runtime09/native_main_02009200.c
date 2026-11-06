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
extern u32 native_fn_02009470();
extern u32 native_fn_02009c54();
u32 native_main_02009200(u32 arg0, u32 arg1, u32 arg2, s32 arg3) {
    s32 var_r4;
    u32 var_r5;

    var_r5 = arg2;
    var_r4 = 0;
    goto loop_4;
block_1:
    if (!(var_r5 & 1)) {
        goto block_3;
    }
    native_fn_02009c54(var_r4);
block_3:
    var_r4 += 1;
    var_r5 = var_r5 >> 1;
loop_4:
    if (var_r4 >= 8) {
        goto block_6;
    }
    if (var_r5 != 0) {
        goto block_1;
    }
block_6:
    return native_fn_02009470(0xD, arg0, arg1, arg2, arg3);
}
