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
extern u32 native_fn_020a4378();
extern u32 native_fn_020a439c();
u32 native_main_020a4078(u32 arg0, s32 arg1, s32 arg2) {
    u32 temp_r4;

    temp_r4 = native_fn_020a4378();
    if (native_fn_020a439c(arg0) == 2) {
        return 0U;
    }
    M2C_FIELD(temp_r4, s32 *, 4) = arg1;
    M2C_FIELD(temp_r4, s32 *, 8) = arg2;
    M2C_FIELD(temp_r4, s8 *, 0x1D) = 1;
    M2C_FIELD(temp_r4, s32 *, 0x10) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x18) = 0;
    return 1U;
}
