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
#define NULL ((void *)0)
extern u32 native_fn_02049008();
extern u8 native_data_ov003_021e0a68[];
extern u8 native_data_ov003_021e0a6c[];
extern u8 native_data_ov003_021e0a70[];
u32 native_ov003_021de97c(void *arg0, s16 arg1, s16 arg2, u8 arg3, s8 arg4, s8 arg5, s8 arg6, s32 arg7, u8 arg8) {
    M2C_FIELD(arg0, s16 *, 0xE) = arg1;
    M2C_FIELD(arg0, s16 *, 0xC) = arg2;
    M2C_FIELD(arg0, s32 *, 0) = arg7;
    M2C_FIELD(arg0, s32 *, 4) = 0;
    native_fn_02049008(arg0, arg3, arg4, arg5, (s32) arg6);
    native_data_ov003_021e0a6c[arg8] = arg3;
    native_data_ov003_021e0a70[arg8] = (u8) arg4;
    native_data_ov003_021e0a68[arg8] = (u8) arg5;
    return (u32) native_data_ov003_021e0a68;
}
