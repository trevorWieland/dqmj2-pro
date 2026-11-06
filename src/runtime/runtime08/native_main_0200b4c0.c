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
extern u32 native_fn_0200a5e0();
extern u32 native_fn_0200a63c();
extern u32 native_fn_0200b218();
extern u32 native_fn_0200b42c();
u32 native_main_0200b4c0(void *arg0) {
    native_fn_0200a5e0(arg0, native_fn_0200a63c(arg0, M2C_FIELD(arg0, s32 *, 0x10)));
    if (native_fn_0200b218(M2C_FIELD(arg0, s32 *, 8)) != 0) {
        native_fn_0200b42c();
    }
    if (M2C_FIELD(arg0, s32 *, 0x14) == 0) {
        return 1U;
    }
    return 0U;
}
