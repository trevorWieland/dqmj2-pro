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
extern u32 native_fn_0204540c();
extern u32 native_fn_02045490();
u32 native_main_0204535c(s32 arg0, u32 arg1, u32 arg2, u32 arg3, s32 arg4) {
    if (arg0 == 0) {
        native_fn_0204540c(arg1, arg2, arg3, arg4);
    } else {
        native_fn_02045490(arg1, arg2, arg3, arg4);
    }
    return 0U;
}
