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
extern u32 native_fn_020b2a38();
u32 native_main_020b2c6c(void **arg0, s32 arg1, u32 arg2) {
    void *temp_r4;

    temp_r4 = *arg0;
    native_fn_020b2a38(temp_r4, arg2, 0x100);
    M2C_FIELD(temp_r4, s32 *, 0x5B8) = arg1;
    return 0x5B8U;
}
