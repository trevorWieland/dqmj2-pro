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
extern u32 native_fn_ov005_021dd8b8();
u32 native_ov005_021dcb9c(void) {
    M2C_FIELD((void *)0x04000008, u16 *, 0) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 0) & 0x43) | 8);
    M2C_FIELD((void *)0x04000008, u16 *, 0) = (u16) (M2C_FIELD((void *)0x04000008, u16 *, 0) & ~3);
    M2C_FIELD((void *)0x04000008, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 2) & ~3) | 2);
    M2C_FIELD((void *)0x04000008, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 4) & ~3) | 2);
    M2C_FIELD((void *)0x04000008, u16 *, 6) = (u16) ((M2C_FIELD((void *)0x04000008, u16 *, 6) & ~3) | 3);
    M2C_FIELD((void *)0x04000008, s32 *, 8) = 0;
    M2C_FIELD((void *)0x04000008, s32 *, 0xC) = 0;
    M2C_FIELD((void *)0x04000008, s32 *, 0x10) = 0;
    M2C_FIELD((void *)0x04000008, s32 *, 0x14) = 0;
    return native_fn_ov005_021dd8b8();
}
