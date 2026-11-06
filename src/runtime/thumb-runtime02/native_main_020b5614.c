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
extern u32 native_fn_020b3b80();
extern u32 native_fn_020b5390();
extern u32 native_fn_020b544c();
u32 native_main_020b5614(void *arg0, u32 arg1, s32 arg2) {
    s32 sp0;

    if (native_fn_020b5390(arg0, 5, arg2 + 7 + M2C_FIELD(M2C_FIELD(arg0, void **, 8), s32 *, 0x44), &sp0) == 0) {
        return 0U;
    }
    if (sp0 != 0) {
        return 1U;
    }
    native_fn_020b3b80(arg0 + 0x50, arg1, arg2);
    if (native_fn_020b544c(arg0) != 0) {
        return 1U;
    }
    return 0U;
}
