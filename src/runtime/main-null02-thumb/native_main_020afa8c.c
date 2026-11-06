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
extern u32 native_fn_020a8b6c();
extern u32 native_fn_020a8b7c();
extern u32 native_fn_020a929c();
u32 native_main_020afa8c(void **arg0, void *arg1) {
    void *temp_r2;
    void *temp_r4;

    temp_r2 = *arg0;
    if (M2C_FIELD(arg1, s32 *, 0) == 3) {
        temp_r4 = M2C_FIELD(arg1, void **, 4);
        M2C_FIELD(temp_r2, s32 *, 0x238) = (s32) (M2C_FIELD(temp_r2, s32 *, 0x238) - 1);
        native_fn_020a8b7c(M2C_FIELD(temp_r4, s32 *, 4), 2);
        native_fn_020a8b6c(M2C_FIELD(temp_r4, s32 *, 4));
        native_fn_020a929c(M2C_FIELD(temp_r4, void **, 0x18));
        M2C_FIELD(temp_r4, void **, 0x18) = NULL;
        native_fn_020a929c(M2C_FIELD(temp_r4, void **, 8));
        M2C_FIELD(temp_r4, void **, 8) = NULL;
    }
    native_fn_020a929c(M2C_FIELD(arg1, void **, 4));
    M2C_FIELD(arg1, void **, 4) = NULL;
    return native_fn_020a929c(arg1);
}
