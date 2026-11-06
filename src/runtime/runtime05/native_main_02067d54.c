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
u32 native_main_02067d54(s32 arg0) {
    if (arg0 < 0x9C4) {
        return 0U;
    }
    if (arg0 < 0x1388) {
        return 1U;
    }
    if (arg0 < 0x1D4C) {
        return 2U;
    }
    if (arg0 < 0x30D4) {
        return 3U;
    }
    if (arg0 < 0x61A8) {
        return 4U;
    }
    if (arg0 < 0xAFC8) {
        return 5U;
    }
    if (arg0 < 0xD6D8) {
        return 6U;
    }
    return 7U;
}
