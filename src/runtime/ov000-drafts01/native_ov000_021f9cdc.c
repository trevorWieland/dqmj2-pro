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
extern u32 native_fn_0204b380();
extern u32 native_fn_02085320();
extern u32 native_fn_ov000_02215698();
extern u32 native_fn_ov000_02217bdc();
u32 native_ov000_021f9cdc(u32 arg0, u32 arg1, u32 arg2, u32 arg3, u32 arg4) {
    u32 temp_r4;
    u32 var_r0;

    temp_r4 = native_fn_ov000_02215698();
    native_fn_02085320(native_fn_ov000_02217bdc(arg0, arg1, arg2, arg3, 1, -1), 0, 1);
    native_fn_0204b380(temp_r4 + 0x10, 0);
    var_r0 = arg4;
    if (var_r0 != 0) {
        var_r0 = 6;
        M2C_FIELD(temp_r4, s8 *, 0x494) = 6;
    }
    return var_r0;
}
