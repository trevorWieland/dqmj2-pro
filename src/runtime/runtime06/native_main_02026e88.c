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
extern u8 native_data_020ec9b8[];
void native_main_02026e88(s32 arg0, s32 arg1, s32 arg2) {
    M2C_FIELD(native_data_020ec9b8, s32 *, 0x10) = (s32) (((0 - arg2) & 0x7FFFF) | (((u32) (arg1 << 0x1C) >> 4) | 0x30000000 | ((u32) (arg0 << 0x1B) >> 8)));
}
