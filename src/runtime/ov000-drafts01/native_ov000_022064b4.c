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
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_02008c58();
extern u32 native_fn_02045738();
extern u32 native_fn_ov000_0220659c();
extern u32 native_fn_ov000_0220668c();
u32 native_ov000_022064b4(void) {
    M2C_FIELD((void *)0x04001008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 0) & 0x43) | 0x11C);
    M2C_FIELD((void *)0x04001008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 2) & 0x43) | 0x14);
    M2C_FIELD((void *)0x04001008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 4) & 0x43) | 0x208);
    M2C_FIELD((void *)0x04001008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04001008, u16 *, 6) & 0x43) | 0x304);
    native_fn_02008c58(0, 0x06200000, 0x20000);
    native_fn_02008c58(0, 0x06600000, 0x20000);
    native_fn_02008c58(0, 0x05000400, 0x400);
    M2C_FIELD((void *)0x04001000, s32 *, 0) = (s32) ((M2C_FIELD((void *)0x04001000, s32 *, 0) & ~0x1F00) | 0x1F00);
    M2C_FIELD((void *)0x04001000, u16 *, 8) = (u16) (M2C_FIELD((void *)0x04001000, u16 *, 8) & ~3);
    M2C_FIELD((void *)0x04001000, u16 *, 0xC) = (u16) ((M2C_FIELD((void *)0x04001000, u16 *, 0xC) & ~3) | 1);
    M2C_FIELD((void *)0x04001000, u16 *, 0xE) = (u16) ((M2C_FIELD((void *)0x04001000, u16 *, 0xE) & ~3) | 2);
    M2C_FIELD((void *)0x04001000, u16 *, 0xA) = (u16) ((M2C_FIELD((void *)0x04001000, u16 *, 0xA) & ~3) | 3);
    native_fn_02045738(1);
    native_fn_ov000_0220659c();
    return native_fn_ov000_0220668c();
}
