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
extern u8 native_data_020f69ec[];
u32 native_main_02045088(s32 arg0, s32 arg1) {
    return ((s32) ((u32) (M2C_FIELD(((arg0 * 0x64) + M2C_FIELD(native_data_020f69ec, s32 *, 4)), u16 *, 6) << 0x10) >> 0x1D) >> arg1) & 1;
}
