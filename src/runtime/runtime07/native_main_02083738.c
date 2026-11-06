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
extern u32 native_fn_020824b4();
extern u32 native_fn_02083764();
extern u8 native_data_021c72a0[];
u32 native_main_02083738(void) {
    native_fn_020824b4(1);
    M2C_FIELD(native_data_021c72a0, u16 *, 0x1A) = (u16) native_fn_02083764(M2C_FIELD(native_data_021c72a0, u16 *, 8));
    return (u32) M2C_FIELD(native_data_021c72a0, u16 *, 0x1A);
}
