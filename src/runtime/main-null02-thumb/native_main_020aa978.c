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
extern u32 native_fn_020a8940();
extern u32 native_fn_020a929c();
extern u32 native_fn_020ade3c();
extern u32 native_fn_020af494();
u32 native_main_020aa978(void **arg0) {
    void *temp_r4;

    temp_r4 = *arg0;
    native_fn_020ade3c(arg0, 1);
    native_fn_020af494(arg0);
    native_fn_020a8940(M2C_FIELD(temp_r4, s32 *, 0x5C8));
    native_fn_020a929c(temp_r4);
    *arg0 = NULL;
    return 0U;
}
