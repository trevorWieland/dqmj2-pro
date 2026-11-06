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
extern u32 native_fn_0203c438();
extern u8 native_data_020edf20[];
u32 native_main_0202ac90(s32 arg0, s16 arg1) {
    M2C_FIELD(native_data_020edf20, s32 *, 8) = arg0;
    M2C_FIELD(native_data_020edf20, s16 *, 4) = arg1;
    M2C_FIELD(native_data_020edf20, s16 *, 6) = 0;
    native_fn_0203c438();
    return 1U;
}
