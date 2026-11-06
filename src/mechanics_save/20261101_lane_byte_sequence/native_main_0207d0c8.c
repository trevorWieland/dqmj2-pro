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
extern u32 native_fn_0207cff4(u32);
u32 native_main_0207d0c8(u32 arg0, u32 arg1) {
    s32 var_r0;

    if (native_fn_0207cff4(arg0) == 0) {
        goto block_4;
    }
    var_r0 = (s32) (arg1 + (arg1 >> 0x1F)) >> 1;
    if (var_r0 >= 1) {
        goto block_3;
    }
    var_r0 = 1;
block_3:
    return (u32) var_r0;
block_4:
    return arg1;
}
