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
extern u32 native_fn_020a929c();
u32 native_main_020af3c8(void *arg0) {
    void *var_r0;

    var_r0 = M2C_FIELD(arg0, void **, 0x10);
    if (var_r0 != NULL) {
        native_fn_020a929c(M2C_FIELD(var_r0, void **, 0));
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 4));
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 4) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 8));
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 8) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0xC));
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0xC) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0x10));
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0x10) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0x14));
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0x14) = NULL;
        native_fn_020a929c(M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0xC8));
        M2C_FIELD(M2C_FIELD(arg0, void **, 0x10), void **, 0xC8) = NULL;
        native_fn_020a929c(M2C_FIELD(arg0, void **, 0x10));
        var_r0 = NULL;
        M2C_FIELD(arg0, void **, 0x10) = NULL;
    }
    return (u32) var_r0;
}
