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
u32 native_ov001_021fcaf8(void *arg0) {
    s8 temp_r2;

    if (M2C_FIELD(arg0, s8 *, 2) == 0) {
        return 2U;
    }
    temp_r2 = M2C_FIELD(arg0, s8 *, 0);
    if (temp_r2 == 2) {
        return 6U;
    }
    if ((temp_r2 == 0) && (M2C_FIELD(arg0, s8 *, 1) == 0)) {
        return 1U;
    }
    if ((temp_r2 == 0) && (M2C_FIELD(arg0, s8 *, 1) == 1)) {
        return 4U;
    }
    if ((temp_r2 == 1) && (M2C_FIELD(arg0, s8 *, 1) == 0)) {
        return 5U;
    }
    if (temp_r2 == 1) {
        return 3U;
    }
    return 0U;
}
