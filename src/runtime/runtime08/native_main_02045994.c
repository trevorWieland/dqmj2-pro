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
extern u32 native_fn_02008430();
extern u32 native_fn_02008bf8();
extern u32 native_fn_02045600();
extern u8 native_data_020f6aec[];
u32 native_main_02045994(u32 arg0, u32 arg1, s32 arg2, u32 arg3) {
    if (arg0 >= 4U) {
        native_fn_02008430();
        return 0U;
    }
    native_fn_02008bf8(arg1, native_data_020f6aec + (arg0 << 0xB) + (arg2 * 2), arg3);
    native_fn_02045600(arg0);
    return 1U;
}
