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
extern u32 native_fn_0200197c();
extern u32 native_fn_02004668();
extern u32 native_fn_02004698();
extern u32 native_fn_0202e300();
u32 native_main_02031ef0(s32 arg0, s32 arg1) {
    u8 sp0[64];

    native_fn_0202e300();
    M2C_FIELD((void *)0x04000440, s32 *, 0) = 0;
    M2C_FIELD((void *)0x04000440, s32 *, 4) = 0;
    M2C_FIELD((void *)0x04000440, s32 *, 0x14) = 0;
    if (arg0 != 0) {
        do {

        } while (native_fn_02004668(&sp0) != 0);
        native_fn_0200197c(&sp0, arg0);
    }
    if (arg1 != 0) {
        do {

        } while (native_fn_02004698(arg1) != 0);
    }
    M2C_FIELD((void *)0x04000448, s32 *, 0) = 1;
    M2C_FIELD((void *)0x04000448, s32 *, -8) = 2;
    return 2U;
}
