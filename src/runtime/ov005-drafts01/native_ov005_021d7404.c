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
u32 native_ov005_021d7404(s32 arg0, u32 arg1, s32 arg2, s32 arg3) {
    u32 var_r1;
    s32 var_r4;
    u32 var_r6;

    var_r1 = arg1;
    if (var_r1 == 0) {
        var_r1 = arg0 + 0x2F4;
    }
    var_r6 = var_r1;
loop_3:
    var_r6 += 0x30;
    if (var_r6 >= (u32) (arg0 + 0x324)) {
        var_r6 = arg0 + 0x24;
    }
    if (M2C_FIELD(var_r6, s32 *, 4) == arg2) {
        var_r4 = 1;
    } else {
        var_r4 = 0;
    }
    if ((arg3 != 0) && (var_r4 != 0)) {

    } else if ((arg3 == 0) && (var_r4 == 0)) {

    } else if (var_r6 == var_r1) {
        var_r6 = 0;
    } else {
        goto loop_3;
    }
    return var_r6;
}
