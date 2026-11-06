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
extern u32 native_fn_ov000_02219d9c();
extern u8 native_data_020f6054[];
u32 native_main_0203eb30(void) {
    M2C_FIELD(native_data_020f6054, s8 *, 8) = 4;
    M2C_FIELD(native_data_020f6054, s8 *, 0xA) = 0x1D;
    native_fn_ov000_02219d9c(1);
    return 0U;
}
