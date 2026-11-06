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
extern u8 native_data_020daffc[];
u32 native_main_02072f1c(s32 arg0) {
    if (arg0 != 0x9995) {
        goto block_2;
    }
    return 0U;
block_2:
    if (arg0 >= 0x200) {
        goto block_4;
    }
    return (u32) (s8) native_data_020daffc[arg0];
block_4:
    return 0U;
}
