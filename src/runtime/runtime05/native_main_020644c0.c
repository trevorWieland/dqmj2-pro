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
extern u32 native_fn_0207dea8();
extern u32 native_fn_0207e3f8();
extern u32 native_fn_020c225c();
u32 native_main_020644c0(void) {
    if (native_fn_0207dea8() != 0) {
        if (native_fn_0207e3f8() != 0) {
            native_fn_020c225c(0x20000000);
        }
        return 1U;
    }
    return 0U;
}
