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
extern u32 native_fn_0202e6fc();
extern u32 native_fn_0202e738();
u32 native_main_020287c4(void *arg0) {
    native_fn_0202e6fc(M2C_FIELD(arg0, u8 *, 0x11), M2C_FIELD(arg0, s16 *, 8), M2C_FIELD(arg0, s16 *, 0xA), M2C_FIELD(arg0, s16 *, 0xC));
    native_fn_0202e738(M2C_FIELD(arg0, u8 *, 0x11), M2C_FIELD(arg0, u16 *, 0xE));
    return 1U;
}
