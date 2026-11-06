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
extern u8 native_data_020dc8bc[];
u32 native_main_020c5968(s32 arg0) {
    u16 var_r3;

    var_r3 = 0;
loop_1:
    if (arg0 != *(u32 *)(native_data_020dc8bc + (var_r3 * 4))) {
        goto block_3;
    }
    return 1U;
block_3:
    var_r3 += 1;
    if ((u32) var_r3 < 0xFU) {
        goto loop_1;
    }
    return 0U;
}
