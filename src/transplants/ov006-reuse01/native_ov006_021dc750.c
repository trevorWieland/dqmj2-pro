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
u32 native_ov006_021dc750(s32 arg0) {
    if (arg0 == 0) {
        return -1U;
    }
    if (arg0 <= 7) {
        return 0U;
    }
    if (arg0 <= 0xE) {
        return 1U;
    }
    if (arg0 <= 0x11) {
        return 2U;
    }
    if (arg0 <= 0x14) {
        return 3U;
    }
    if (arg0 <= 0x18) {
        return 4U;
    }
    if (arg0 <= 0x1E) {
        return 5U;
    }
    if (arg0 <= 0x23) {
        return 6U;
    }
    if (arg0 <= 0x27) {
        return 7U;
    }
    if (arg0 <= 0x2F) {
        return 8U;
    }
    return -1U;
}
