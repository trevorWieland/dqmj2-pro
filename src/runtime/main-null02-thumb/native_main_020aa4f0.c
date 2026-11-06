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
extern u32 native_fn_020b0a50();
u32 native_main_020aa4f0(void **arg0, u32 arg1, s32 *arg2) {
    s32 *temp_r0;
    s32 *temp_r0_2;
    void *temp_r3;
    void *sp0;

    if ((arg0 == NULL) || (temp_r3 = *arg0, (temp_r3 == NULL))) {
        return 2U;
    }
    if (M2C_FIELD(temp_r3, s32 *, 0x108) != 0) {
        *arg2 = 0;
        return 0U;
    }
    if ((native_fn_020b0a50(arg0, arg1, &sp0) != 0) && (temp_r0 = M2C_FIELD(sp0, s32 **, 8), (temp_r0 != NULL))) {
        *arg2 = *temp_r0;
    } else if ((native_fn_020b0a50(arg0, arg1, &sp0) != 0) && (temp_r0_2 = M2C_FIELD(sp0, s32 **, 0xC), (temp_r0_2 != NULL))) {
        *arg2 = *temp_r0_2;
    } else {
        *arg2 = -1;
    }
    return 0U;
}
