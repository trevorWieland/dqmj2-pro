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
extern u32 native_fn_02042c0c();
u32 native_ov000_021e8468(void *arg0) {
    s16 temp_r1;

    if (M2C_FIELD(arg0, u8 *, 0x2A8) == 0) {
        M2C_FIELD(arg0, s16 *, 0x2AC) = 0x1F;
        M2C_FIELD(arg0, u8 *, 0x2A8) = 0xAU;
    }
    temp_r1 = M2C_FIELD(arg0, s16 *, 0x2AC);
    if ((s32) temp_r1 <= 0) {
        M2C_FIELD(arg0, s8 *, 0x2A9) = 3;
        return 1U;
    }
    native_fn_02042c0c(arg0, (u8) temp_r1);
    M2C_FIELD(arg0, s16 *, 0x2AC) = (s16) (M2C_FIELD(arg0, s16 *, 0x2AC) - 1);
    return 0U;
}
