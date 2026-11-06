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
extern u32 native_fn_02008c58();
u32 native_main_020c3e9c(void) {
    u32 temp_r0;

    M2C_FIELD((void *)0x04001008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 0) & 0x43) | 0x108);
    M2C_FIELD((void *)0x04001008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 2) & 0x43) | 4);
    M2C_FIELD((void *)0x04001008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 4) & 0x43) | 0x218);
    M2C_FIELD((void *)0x04001008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 6) & 0x43) | 0x310);
    native_fn_02008c58(0, 0x06200000, 0x20000);
    native_fn_02008c58(0, 0x06600000, 0x20000);
    native_fn_02008c58(0, 0x05000400, 0x400);
    native_fn_02008c58(0, 0x07000400, 0x400);
    M2C_FIELD((void *)0x0400100C, u16 *, 0) = (u16) (M2C_FIELD((void *)0x0400100C, u16 *, 0) & ~3);
    M2C_FIELD((void *)0x04001008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 0) & ~3) | 1);
    *(u16 *)0x0400100A = (*(u16 *)0x0400100A & ~3) | 2;
    M2C_FIELD((void *)0x0400100C, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x0400100C, u16 *, 2) & ~3) | 3);
    temp_r0 = (*(u32 *)0x04001000 & ~0x1F00) | 0x1F00;
    *(u32 *)0x04001000 = temp_r0;
    return temp_r0;
}
