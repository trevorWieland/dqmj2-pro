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
extern u32 native_fn_0201d444();
extern u8 native_data_020dd9dc[];
extern u8 native_data_020ddaa8[];
extern u8 native_data_020f69f4[];
u32 native_main_02044d30(s32 arg0) {
    native_fn_0201d444(native_data_020f69f4, native_data_020ddaa8, native_data_020dd9dc + (arg0 * 5));
    return (u32) native_data_020f69f4;
}
