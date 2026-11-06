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
extern u8 native_data_020e68c0[];
u32 native_main_02016700(void) {
    M2C_FIELD(native_data_020e68c0, s8 *, 0x25) = 0;
    M2C_FIELD(native_data_020e68c0, s8 *, 0x26) = 0;
    M2C_FIELD(native_data_020e68c0, s8 *, 0x27) = 0;
    M2C_FIELD(native_data_020e68c0, s8 *, 0x28) = 0;
    M2C_FIELD(native_data_020e68c0, s8 *, 0x29) = 0;
    return (u32) native_data_020e68c0;
}
