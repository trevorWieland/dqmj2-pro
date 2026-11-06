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
extern u32 native_fn_0207c3d8();
u32 native_main_0207c11c(void *arg0, s32 arg1, u32 arg2) {
    s16 temp_r0;
    s16 temp_r2;

    temp_r2 = (s16) native_fn_0207c3d8(arg0, arg2);
    M2C_FIELD(arg0, s16 *, 6) = (s16) (M2C_FIELD(arg0, s16 *, 6) + arg1);
    if ((s32) M2C_FIELD(arg0, s16 *, 6) >= 0) {
        goto block_2;
    }
    M2C_FIELD(arg0, s16 *, 6) = 0;
block_2:
    temp_r0 = M2C_FIELD(arg0, s16 *, 6);
    if ((s32) temp_r0 <= (s32) temp_r2) {
        goto block_4;
    }
    M2C_FIELD(arg0, s16 *, 6) = temp_r2;
block_4:
    return (u32) temp_r0;
}
