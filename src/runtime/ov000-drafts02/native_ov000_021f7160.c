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
void native_ov000_021f7160(void) {
    M2C_FIELD((void *)0x0400000A, u16 *, 0) = (u16) (M2C_FIELD((void *)0x0400000A, u16 *, 0) & ~3);
    M2C_FIELD((void *)0x0400000A, u16 *, 4) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 4) & ~3) | 3);
    M2C_FIELD((void *)0x0400000A, u16 *, 2) = (u16) ((M2C_FIELD((void *)0x0400000A, u16 *, 2) & ~3) | 2);
    *(u16 *)0x04000008 = (*(u16 *)0x04000008 & ~3) | 1;
}
