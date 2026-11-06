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
extern u32 native_fn_020a8614();
extern u32 native_fn_020a8940();
extern u32 native_fn_020a8b6c();
extern u32 native_fn_020a8ef4();
extern u32 native_fn_020a929c();
u32 native_main_020b5b4c(void *arg0) {
    if (M2C_FIELD(arg0, s32 *, 0x1C) != 0) {
        M2C_FIELD(arg0, s32 *, 0x14) = 1;
        return 1U;
    }
    native_fn_020a8b6c(M2C_FIELD(arg0, s32 *, 0));
    native_fn_020a8940(M2C_FIELD(arg0, s32 *, 0xC));
    native_fn_020a8614(M2C_FIELD(arg0, s32 *, 0x10));
    native_fn_020a929c(arg0);
    return native_fn_020a8ef4();
}
