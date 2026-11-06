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
u32 native_ov000_021e34b8(void *arg0, s8 arg1, s8 arg2, s8 arg3, u8 arg4, s8 arg5, u8 arg6, s32 arg7, s32 arg8) {
    M2C_FIELD(arg0, s8 *, 0x23) = arg1;
    M2C_FIELD(arg0, s8 *, 0x27) = arg2;
    M2C_FIELD(arg0, s8 *, 0x2C) = arg3;
    M2C_FIELD(arg0, u8 *, 0x29) = arg4;
    M2C_FIELD(arg0, s8 *, 0x2A) = arg5;
    M2C_FIELD(arg0, u8 *, 0x2B) = arg6;
    M2C_FIELD(arg0, s16 *, 0x2E) = (s16) arg7;
    M2C_FIELD(arg0, s16 *, 0x30) = (s16) arg8;
    return (u32) arg0;
}
