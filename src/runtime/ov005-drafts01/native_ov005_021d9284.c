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
u32 native_ov005_021d9284(void *arg0, s32 arg1, s32 arg2) {
    void *temp_lr;

    temp_lr = M2C_FIELD(M2C_FIELD(M2C_FIELD(arg0, void **, 0x20), void **, 0xC), void **, 0x24);
    M2C_FIELD(arg0, s32 *, 0) = 0;
    M2C_FIELD(arg0, s32 *, 4) = 0;
    M2C_FIELD(arg0, s32 *, 8) = 0;
    M2C_FIELD(arg0, s16 *, 0xC) = 0;
    M2C_FIELD(arg0, s32 *, 0x10) = 0;
    M2C_FIELD(arg0, s32 *, 0x14) = 0;
    M2C_FIELD(arg0, s32 *, 0x18) = 0;
    M2C_FIELD(arg0, s16 *, 0x1C) = 0;
    M2C_FIELD(temp_lr, s32 *, 4) = arg1;
    M2C_FIELD(temp_lr, s32 *, 8) = arg2;
    M2C_FIELD(temp_lr, s32 *, 0x10) = 1;
    M2C_FIELD(temp_lr, s32 *, 0x14) = 0;
    M2C_FIELD(temp_lr, s32 *, 0x18) = 0;
    M2C_FIELD(temp_lr, s32 *, 0xC) = 1;
    return (u32) arg0;
}
