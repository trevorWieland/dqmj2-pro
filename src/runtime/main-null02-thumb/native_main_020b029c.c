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
extern u32 native_fn_020a8614();
extern u32 native_fn_020a929c();
u32 native_main_020b029c(u32 arg0, void *arg1) {
    native_fn_020a929c(M2C_FIELD(arg1, void **, 0x1C));
    M2C_FIELD(arg1, void **, 0x1C) = NULL;
    native_fn_020a929c(M2C_FIELD(arg1, void **, 0x2C));
    M2C_FIELD(arg1, void **, 0x2C) = NULL;
    if (M2C_FIELD(arg1, s32 *, 0x3C) != 0) {
        native_fn_020a8614();
        M2C_FIELD(arg1, s32 *, 0x3C) = 0;
    }
    return native_fn_020a929c(arg1);
}
