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
u32 native_ov005_021d9228(void *arg0, void *arg1) {
    void *temp_r2;
    s32 *temp_r3;

    temp_r2 = M2C_FIELD(arg0, void **, 0x20);
    temp_r3 = M2C_FIELD(M2C_FIELD(temp_r2, void **, 0xC), s32 **, 0x24);
    *temp_r3 = M2C_FIELD(temp_r2, s32 *, 0x14);
    M2C_FIELD(arg1, s32 **, 0) = temp_r3;
    M2C_FIELD(arg1, s16 *, 4) = 4;
    return 4U;
}
