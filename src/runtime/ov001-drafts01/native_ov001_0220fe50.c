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
u32 native_ov001_0220fe50(u32 arg0) {
    switch (arg0) {
    case 0x200:
        return 0xAU;
    case 0x800000:
        return 0x31U;
    case 0x8:
        return 0xBU;
    case 0x10:
        return 0xCU;
    case 0x1000000:
        return 0x43U;
    case 0x20:
        return 0x3FU;
    default:
        return 0U;
    }
}
