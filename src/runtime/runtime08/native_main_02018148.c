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
u32 native_main_02018148(u32 arg0, u32 arg1, s32 arg2) {
    if ((arg0 > 0x1FEU) || (arg0 < 0xE4U)) {
        return 0U;
    }
    if ((arg1 > 0x10U) || (arg1 < 8U)) {
        return 0U;
    }
    if ((s32) ((arg2 * (((arg1 + 0x20) * 4) + 0x70)) + (((arg0 + 0x26) * 4) + 0x14A)) < 0x15E0) {
        return 1U;
    }
    return 0U;
}
