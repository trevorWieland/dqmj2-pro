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
extern u32 native_fn_02048f1c();
extern u32 native_fn_02048f2c();
extern u32 native_fn_02048f3c();
extern u32 native_fn_02048f4c();
extern u32 native_fn_02048f7c();
extern u32 native_fn_0205fdcc();
extern u32 native_fn_020c484c();
extern u32 native_fn_020c4960();
extern u32 native_fn_020ccb90();
extern u32 native_fn_020cd580();
u32 native_main_020cc3fc(void) {
    native_fn_020cd580();
    native_fn_020ccb90();
    native_fn_020c4960();
    native_fn_0205fdcc(1);
    native_fn_02048f3c(2, 1);
    native_fn_02048f2c(0, 1);
    native_fn_02048f1c(1, 1);
    native_fn_02048f4c(3, 1);
    M2C_FIELD((void *)0x0400100C, u16 *, 0) = (u16) (M2C_FIELD((void *)0x0400100C, u16 *, 0) & ~3);
    *(u16 *)0x04001008 = (*(u16 *)0x04001008 & ~3) | 1;
    *(u16 *)0x0400100A = (*(u16 *)0x0400100A & ~3) | 2;
    M2C_FIELD((void *)0x0400100C, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x0400100C, u16 *, 2) & ~3) | 3);
    native_fn_02048f7c(1);
    return native_fn_020c484c();
}
