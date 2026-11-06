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
extern u32 native_fn_ov006_021e8814();
u32 native_ov006_021e8a28(s32 arg0, u32 arg1, u32 arg2) {
    u32 var_r4;

    var_r4 = arg0 + 1;
    if (var_r4 >= arg1) {
        var_r4 = 0;
    }
    native_fn_ov006_021e8814(arg0, var_r4, arg1, arg2);
    return var_r4;
}
