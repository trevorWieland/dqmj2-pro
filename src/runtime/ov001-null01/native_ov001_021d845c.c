#define NULL ((void *)0)
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
u32 native_ov001_021d845c(void *arg0) {
    u32 temp_r0;
    void *temp_r3;

    temp_r3 = M2C_FIELD(arg0, void **, 0xB0);
    if (temp_r3 == NULL) {
        return (u32) arg0;
    }
    temp_r0 = (M2C_FIELD(temp_r3, u32 *, 4) & ~0xFFFF) | (M2C_FIELD(M2C_FIELD(M2C_FIELD(arg0, void **, 4), void **, 0x2C), u16 *, 0x15C) | 0x8000);
    M2C_FIELD(temp_r3, u32 *, 4) = temp_r0;
    return temp_r0;
}
