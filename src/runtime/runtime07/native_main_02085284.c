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
extern u32 native_fn_0205dc70();
u32 native_main_02085284(void *arg0, u8 arg1, u8 arg2, u16 arg3) {
    u32 temp_r0;

    M2C_FIELD(arg0, u8 *, 0) = arg1;
    M2C_FIELD(arg0, u8 *, 1) = arg2;
    M2C_FIELD(arg0, u16 *, 2) = arg3;
    temp_r0 = native_fn_0205dc70(M2C_FIELD(arg0, u8 *, 0), M2C_FIELD(arg0, u8 *, 1), M2C_FIELD(arg0, u16 *, 2));
    M2C_FIELD(arg0, u32 *, 0x2C) = temp_r0;
    return temp_r0;
}
