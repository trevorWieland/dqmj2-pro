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
extern u32 native_fn_020b0b48();
u32 native_main_020add5c(void **arg0, void *arg1) {
    void *temp_r1;
    void *temp_r1_2;
    void *temp_r4;

    temp_r1 = M2C_FIELD(arg1, void **, 8);
    temp_r4 = *arg0;
    if ((temp_r1 != NULL) && (M2C_FIELD(temp_r4, s32 *, 0x104) == 0)) {
        native_fn_020a929c(M2C_FIELD(temp_r1, void **, 8));
        M2C_FIELD(M2C_FIELD(arg1, void **, 8), void **, 8) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg1, void **, 8), void **, 0xC));
        M2C_FIELD(M2C_FIELD(arg1, void **, 8), void **, 0xC) = NULL;
        native_fn_020a929c(M2C_FIELD(arg1, void **, 8));
        M2C_FIELD(arg1, void **, 8) = NULL;
    }
    temp_r1_2 = M2C_FIELD(arg1, void **, 0xC);
    if ((temp_r1_2 != NULL) && (M2C_FIELD(temp_r4, s32 *, 0x104) == 0)) {
        native_fn_020a929c(M2C_FIELD(temp_r1_2, void **, 8));
        M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), void **, 8) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), void **, 0xC));
        M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), void **, 0xC) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), void **, 0x10));
        M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), void **, 0x10) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), void **, 0x14));
        M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), void **, 0x14) = NULL;
        if (M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), s32 *, 0x38) != 0) {
            native_fn_020a8614();
            M2C_FIELD(M2C_FIELD(arg1, void **, 0xC), s32 *, 0x38) = 0;
        }
        native_fn_020a929c(M2C_FIELD(arg1, void **, 0xC));
        M2C_FIELD(arg1, void **, 0xC) = NULL;
    }
    native_fn_020a929c(M2C_FIELD(arg1, void **, 0x14));
    M2C_FIELD(arg1, void **, 0x14) = NULL;
    native_fn_020a929c(M2C_FIELD(arg1, void **, 0x1C));
    M2C_FIELD(arg1, void **, 0x1C) = NULL;
    M2C_FIELD(arg1, s32 *, 0x18) = 0;
    if ((M2C_FIELD(arg1, s32 *, 0x10) == 0) || ((M2C_FIELD(temp_r4, s32 *, 0x104) == 1) && (M2C_FIELD(arg1, void **, 8) == NULL) && (M2C_FIELD(arg1, void **, 0xC) == NULL))) {
        native_fn_020b0b48(arg0, arg1);
        return 0U;
    }
    return 1U;
}
