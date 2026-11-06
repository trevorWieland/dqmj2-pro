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
extern u32 native_fn_020a88d4();
extern u32 native_fn_020b0810();
extern u32 native_fn_020b081c();
extern u32 native_fn_020b0824();
u32 native_main_020b08c8(void **arg0) {
    void *temp_r4;

    temp_r4 = *arg0;
    M2C_FIELD(temp_r4, s32 *, 0x5D0) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x5CC) = 0;
    M2C_FIELD(temp_r4, u32 *, 0x5C8) = native_fn_020a88d4(0x20, 4, native_fn_020b0810, native_fn_020b081c, native_fn_020b0824);
    if (M2C_FIELD(temp_r4, u32 *, 0x5C8) != 0) {
        return 1U;
    }
    return 0U;
}
