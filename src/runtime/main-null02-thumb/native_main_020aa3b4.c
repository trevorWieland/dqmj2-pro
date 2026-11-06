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
u32 native_main_020aa3b4(void **arg0, s32 *arg1) {
    void *temp_r2;

    if ((arg0 == NULL) || (temp_r2 = *arg0, (temp_r2 == NULL))) {
        return 2U;
    }
    if (M2C_FIELD(temp_r2, s32 *, 0x108) != 0) {
        *arg1 = 0;
        return 0U;
    }
    *arg1 = M2C_FIELD(temp_r2, s32 *, 0x5D0);
    return 0U;
}
