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
extern u32 native_fn_0201d800();
u32 native_main_020b0b5c(u32 arg0, void *arg1, void *arg2) {
    void *temp_r4;

    temp_r4 = M2C_FIELD(arg1, void **, 0x10);
    if ((temp_r4 != NULL) && (native_fn_0201d800(M2C_FIELD(arg2, s32 *, 0), M2C_FIELD(temp_r4, s32 *, 0)) == 0) && (native_fn_0201d800(M2C_FIELD(arg2, s32 *, 4), M2C_FIELD(temp_r4, s32 *, 8)) == 0)) {
        *M2C_FIELD(arg2, void ***, 8) = arg1;
        M2C_FIELD(arg2, s32 *, 0xC) = 1;
        return 0U;
    }
    return 1U;
}
