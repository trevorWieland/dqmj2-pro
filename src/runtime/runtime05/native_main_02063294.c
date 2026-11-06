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
extern u8 native_data_021bd524[];
u32 native_main_02063294(s32 arg0) {
    s8 var_r3;

    var_r3 = 0;
loop_1:
    if (arg0 == M2C_FIELD(&native_data_021bd524[var_r3], u8 *, 0x134)) {
        return 1U;
    }
    var_r3 += 1;
    if ((s32) var_r3 >= 0xC) {
        return 0U;
    }
    goto loop_1;
}
