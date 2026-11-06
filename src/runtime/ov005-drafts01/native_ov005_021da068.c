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
extern u32 native_fn_02008c14();
u32 native_ov005_021da068(void *arg0, s32 arg1, s32 arg2) {
    void *temp_r4;

    temp_r4 = M2C_FIELD(M2C_FIELD(M2C_FIELD(arg0, void **, 0x20), void **, 0xC), void **, 0x24);
    M2C_FIELD(temp_r4, s16 *, 0x584) = (s16) (arg1 - 4);
    M2C_FIELD(temp_r4, s16 *, 0x586) = (s16) (arg2 - 4);
    native_fn_02008c14(0, temp_r4 + 0x42C, 0x158);
    M2C_FIELD(temp_r4, s32 *, 0x424) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x420) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x428) = 0;
    M2C_FIELD(temp_r4, s32 *, 0x58C) = 1;
    return 1U;
}
