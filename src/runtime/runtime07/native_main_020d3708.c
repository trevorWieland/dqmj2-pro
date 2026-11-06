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
extern u8 native_data_021d71ec[];
u32 native_main_020d3708(s16 arg0, s8 arg1, s16 arg2, s8 arg3, s32 arg4, u32 arg5) {
    M2C_FIELD(native_data_021d71ec, s16 *, 0x10) = arg0;
    M2C_FIELD(native_data_021d71ec, s8 *, 0x12) = arg1;
    M2C_FIELD(native_data_021d71ec, s16 *, 0x16) = arg2;
    M2C_FIELD(native_data_021d71ec, s8 *, 0x18) = arg3;
    M2C_FIELD(native_data_021d71ec, s16 *, 0x1C) = (s16) arg4;
    M2C_FIELD(native_data_021d71ec, s8 *, 0x1E) = (s8) arg5;
    return arg5;
}
