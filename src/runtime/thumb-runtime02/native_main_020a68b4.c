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
extern u32 native_fn_020a834c();
extern u32 native_fn_020a8c84();
u32 native_main_020a68b4(s32 arg0, u32 arg1, s32 arg2, u32 arg3, s32 arg4) {
    return native_fn_020a834c(arg0 + 0x4C, native_fn_020a8c84(arg1), (u16) ((u8) (arg2 >> 8) | (0xFF00 & (arg2 << 8))), arg3, arg4);
}
