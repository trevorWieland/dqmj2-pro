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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
u32 native_ov006_021e3b7c(u32 arg0) {
    if (arg0 == 0) {
        return 9U;
    }
    if (arg0 == 1) {
        return 0U;
    }
    if (arg0 <= 0xAU) {
        return 1U;
    }
    if (arg0 <= 0x32U) {
        return 2U;
    }
    if (arg0 <= 0x64U) {
        return 3U;
    }
    if (arg0 <= 0x3E8U) {
        return 4U;
    }
    if (arg0 <= 0x1388U) {
        return 5U;
    }
    if (arg0 <= 0x2710U) {
        return 6U;
    }
    if (arg0 <= 0xC350U) {
        return 7U;
    }
    if (arg0 <= 0x186A0U) {
        return 8U;
    }
    return 9U;
}
