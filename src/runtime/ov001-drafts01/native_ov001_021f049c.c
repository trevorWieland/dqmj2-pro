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
extern u32 native_fn_0207b02c();
extern u32 native_fn_0207b674();
extern u32 native_fn_ov001_0220ee0c();
u32 native_ov001_021f049c(u32 arg0, u32 arg1, void *arg2, void *arg3, s32 arg4, s32 arg5, s32 arg6) {
    u32 var_r5;

    var_r5 = arg0;
    if ((arg6 == 0) && (native_fn_ov001_0220ee0c(M2C_FIELD(arg2, s32 *, 0x1E8) + 0x46, arg4, arg1) != 0)) {
        var_r5 = 0;
    }
    if ((native_fn_0207b02c(arg1, 0x80000200) != 0) && ((s32) M2C_FIELD(arg2, s8 *, 0x234) < 3)) {
        var_r5 = 0;
    }
    if ((arg4 == 0) && (arg5 == 0)) {

    } else if ((s32) native_fn_0207b674(0x3B, M2C_FIELD(arg3, s32 *, 0x1E8) + 0x46) > 0) {
        var_r5 = 0;
    }
    return var_r5;
}
