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
extern u32 native_fn_020652f4();
extern u32 native_fn_ov001_021d8498();
extern u32 native_fn_ov001_021d8788();
extern u32 native_fn_ov001_021d8828();
u32 native_ov001_021d8ab0(s32 arg0) {
    s32 var_r5;
    u32 var_r4;

    var_r5 = arg0;
    var_r4 = 0;
    if (var_r5 < 0) {
        var_r5 = (s32) native_fn_020652f4();
    }
    if ((native_fn_ov001_021d8498(var_r5) != 0) && (native_fn_ov001_021d8788(var_r5) != 0) && (native_fn_ov001_021d8828(var_r5) != 0)) {
        var_r4 = 1;
    }
    return var_r4;
}
