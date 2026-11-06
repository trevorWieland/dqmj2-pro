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
extern u32 native_fn_0206dcd0();
extern u8 native_data_021c50e8[];
u32 native_main_02071b9c(void) {
    native_fn_0206dcd0(0);
    M2C_FIELD(native_data_021c50e8, s8 *, 0xD1) = (s8) (M2C_FIELD(native_data_021c50e8, s8 *, 0xD1) | 8);
    return (u32) native_data_021c50e8;
}
