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
extern u32 native_fn_02090a3c();
extern u32 native_fn_02091690();
extern u32 native_fn_02091864();
extern u32 native_fn_020918a4();
u32 native_main_02091a34(void *arg0, u32 arg1) {
    native_fn_02091690(arg0, arg1, M2C_FIELD(arg0, s32 *, 0x81C));
    native_fn_02091864(arg0);
    native_fn_02090a3c(arg0, 0, 0);
    native_fn_020918a4(arg0);
    M2C_FIELD(arg0, s8 *, 0x455) = 5;
    return 0x455U;
}
