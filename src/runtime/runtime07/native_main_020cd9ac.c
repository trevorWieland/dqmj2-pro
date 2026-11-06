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
extern u32 native_fn_02041538();
extern u8 native_data_021d6964[];
u32 native_main_020cd9ac(void) {
    native_fn_02041538(1, 2, 0xA);
    M2C_FIELD(native_data_021d6964, s32 *, 0xC) = 4;
    return (u32) native_data_021d6964;
}
