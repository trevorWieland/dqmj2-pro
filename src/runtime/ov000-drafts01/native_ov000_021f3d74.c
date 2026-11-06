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
extern u32 native_fn_02041f90();
extern u32 native_fn_ov000_021e784c();
u32 native_ov000_021f3d74(u32 arg0, u32 arg1) {
    s32 temp_r0;
    u32 var_r4;

    var_r4 = 0;
    temp_r0 = (s32) native_fn_ov000_021e784c(arg1);
    if (temp_r0 < 0x168000) {
        native_fn_02041f90(arg0, temp_r0, 1);
        var_r4 = 1;
    }
    return var_r4;
}
