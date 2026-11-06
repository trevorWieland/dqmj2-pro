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
extern u8 native_data_021d18cc[];
u32 native_main_020946ec(s32 arg0) {
    if (1 & arg0) {
        return M2C_FIELD(native_data_021d18cc, u32 *, 0xC);
    }
    if (2 & arg0) {
        return M2C_FIELD(native_data_021d18cc, u32 *, 0);
    }
    if (4 & arg0) {
        return M2C_FIELD(native_data_021d18cc, u32 *, 4);
    }
    if (8 & arg0) {
        return M2C_FIELD(native_data_021d18cc, u32 *, 8);
    }
    if (arg0 & 0x10) {
        return M2C_FIELD(native_data_021d18cc, u32 *, 0x10);
    }
    return 0U;
}
