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
extern u32 native_fn_02008e0c();
u32 native_main_0208fb94(s32 arg0, s32 arg1, void *arg2) {
    s32 temp_r0;
    s32 var_r4;
    s32 var_r6;

    var_r4 = M2C_FIELD(arg2, s32 *, 0x14);
    var_r6 = M2C_FIELD(arg2, s32 *, 0x1C);
    if (var_r4 > arg1) {
        var_r4 = arg1;
        var_r6 = 0;
    } else {
        temp_r0 = arg1 - var_r4;
        if (var_r6 > temp_r0) {
            var_r6 = temp_r0;
        }
    }
    if (var_r4 > 0) {
        native_fn_02008e0c(M2C_FIELD(arg2, s32 *, 0x10), arg0, var_r4);
        M2C_FIELD(arg2, s32 *, 0x10) = (s32) (M2C_FIELD(arg2, s32 *, 0x10) + var_r4);
        M2C_FIELD(arg2, s32 *, 0x14) = (s32) (M2C_FIELD(arg2, s32 *, 0x14) - var_r4);
    }
    if (var_r6 > 0) {
        native_fn_02008e0c(M2C_FIELD(arg2, s32 *, 0x18), arg0 + var_r4, var_r6);
        M2C_FIELD(arg2, s32 *, 0x18) = (s32) (M2C_FIELD(arg2, s32 *, 0x18) + var_r6);
        M2C_FIELD(arg2, s32 *, 0x1C) = (s32) (M2C_FIELD(arg2, s32 *, 0x1C) - var_r6);
    }
    return var_r4 + var_r6;
}
