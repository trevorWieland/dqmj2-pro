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
extern u32 native_fn_02008d78();
extern u8 native_data_021d6b48[];
extern u8 native_data_021d6b54[];
u32 native_main_020cf7fc(void) {
    native_fn_02008d78(native_data_021d6b54, 0, 8);
    M2C_FIELD(native_data_021d6b48, s32 *, 8) = 0;
    M2C_FIELD(native_data_021d6b48, s32 *, 4) = 0;
    M2C_FIELD(native_data_021d6b48, u8 *, 0) = 1;
    return (u32) native_data_021d6b48;
}
