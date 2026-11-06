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
extern u32 native_fn_0201b19c();
extern u32 native_fn_0201d69c();
u32 native_main_020b3b80(void *arg0, s32 arg1, u32 arg2) {
    void *var_r0;
    u32 var_r4;
    void *temp_r5;

    var_r0 = arg0;
    temp_r5 = var_r0;
    var_r4 = arg2;
    if ((arg1 != 0) && (var_r4 != 0)) {
        if (var_r4 == -1U) {
            var_r4 = native_fn_0201d69c(arg1);
        }
        native_fn_0201b19c(M2C_FIELD(temp_r5, s32 *, 0) + M2C_FIELD(temp_r5, s32 *, 8), arg1, var_r4);
        var_r0 = M2C_FIELD(temp_r5, s32 *, 8) + var_r4;
        M2C_FIELD(temp_r5, void **, 8) = var_r0;
    }
    return (u32) var_r0;
}
