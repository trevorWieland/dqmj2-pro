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
extern u32 native_fn_0207cff4();
u32 native_main_0207d1e4(u32 arg0, s32 arg1) {
    s32 temp_r1;
    s32 var_r4;

    var_r4 = arg1;
    if (native_fn_0207cff4() == 0) {
        goto block_2;
    }
    temp_r1 = var_r4 * 5;
    var_r4 = (s32) (temp_r1 + ((u32) (temp_r1 >> 1) >> 0x1E)) >> 2;
block_2:
    return (u32) var_r4;
}
