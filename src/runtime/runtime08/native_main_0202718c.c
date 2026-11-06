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
extern u32 native_fn_0202a670();
extern u32 native_fn_0202a7a0();
extern u32 native_fn_02066bdc();
extern u32 native_fn_02066c20();
u32 native_main_0202718c(void) {
    if (((s32) (*(u16 *)0x027FFFA8 & 0x8000) >> 0xF) == 0) {
        native_fn_0202a670();
        native_fn_02066bdc();
        return 1U;
    }
    native_fn_0202a7a0();
    native_fn_02066c20();
    return 0U;
}
