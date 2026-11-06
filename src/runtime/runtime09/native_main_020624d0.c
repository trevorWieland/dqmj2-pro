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
extern u32 native_fn_020620b4();
extern u32 native_fn_02062134();
extern u32 native_fn_02062358();
extern u32 native_fn_020624b0();
extern u32 native_fn_02062520();
u32 native_main_020624d0(u32 arg0, u32 arg1, u32 arg2, u32 arg3) {
    if (native_fn_02062520() != 0) {
        goto block_2;
    }
    return 0U;
block_2:
    native_fn_020620b4(arg0);
    native_fn_02062134(arg3);
    native_fn_020624b0(arg0, arg1);
    native_fn_02062358(arg2);
    return 1U;
}
