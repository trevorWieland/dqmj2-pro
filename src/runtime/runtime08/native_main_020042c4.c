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
u32 native_main_020042c4(s32 *arg0, s32 arg1, s32 arg2, s32 arg3, s32 arg4) {
    *arg0 = arg1 | 0x40 | (arg2 << 8) | ((arg3 | (arg4 << 8)) << 0x10);
    return (u32) arg0;
}
