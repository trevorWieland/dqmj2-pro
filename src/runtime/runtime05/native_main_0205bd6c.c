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
extern u8 native_data_02102dc0[];
u32 native_main_0205bd6c(s8 arg0, s16 arg1, s16 arg2, s16 arg3, u8 arg4, u8 arg5, s16 arg6, u8 arg7, u8 arg8, u8 arg9, u8 argA, s8 argB, u8 argC, u8 argD, s32 argE, s32 argF, s32 arg10, u32 arg11) {
    M2C_FIELD(native_data_02102dc0, s8 *, 0x5C) = arg0;
    M2C_FIELD(native_data_02102dc0, s16 *, 0x54) = arg1;
    M2C_FIELD(native_data_02102dc0, s16 *, 0x56) = arg2;
    M2C_FIELD(native_data_02102dc0, s16 *, 0x58) = arg3;
    M2C_FIELD(native_data_02102dc0, s8 *, 0x61) = (s8) arg6;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x5D) = arg4;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x5E) = arg5;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x5F) = arg7;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x62) = arg8;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x63) = arg9;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x64) = argA;
    M2C_FIELD(native_data_02102dc0, s8 *, 0x65) = argB;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x66) = argC;
    M2C_FIELD(native_data_02102dc0, u8 *, 0x60) = argD;
    M2C_FIELD(native_data_02102dc0, s8 *, 0x67) = (s8) argE;
    M2C_FIELD(native_data_02102dc0, s8 *, 0x68) = (s8) argF;
    M2C_FIELD(native_data_02102dc0, s8 *, 0x69) = (s8) arg10;
    M2C_FIELD(native_data_02102dc0, s8 *, 0x6A) = (s8) arg11;
    return arg11;
}
