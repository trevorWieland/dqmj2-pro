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
extern u32 native_fn_02049008();
extern u8 native_data_ov000_02247704[];
u32 native_ov000_0222b2e8(void *arg0, s16 arg1, s16 arg2, s8 arg3, s8 arg4, s8 arg5) {
    M2C_FIELD(arg0, s16 *, 0xE) = arg1;
    M2C_FIELD(arg0, s16 *, 0xC) = arg2;
    M2C_FIELD(arg0, s32 *, 0) = 0;
    M2C_FIELD(arg0, s32 *, 4) = 0;
    native_fn_02049008(arg0, arg3, arg4, arg5, 2);
    M2C_FIELD(native_data_ov000_02247704, s8 *, 1) = arg3;
    M2C_FIELD(native_data_ov000_02247704, s8 *, 3) = arg4;
    M2C_FIELD(native_data_ov000_02247704, s8 *, 2) = arg5;
    return (u32) native_data_ov000_02247704;
}
