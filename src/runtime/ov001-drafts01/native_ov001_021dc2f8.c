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
extern u32 native_fn_ov001_021db438();
extern u32 native_fn_ov001_021db508();
u32 native_ov001_021dc2f8(s32 arg0) {
    s32 var_r5;
    s32 var_r5_2;
    u32 var_r6;

    var_r6 = 0;
    var_r5 = 0;
loop_1:
    if (arg0 == native_fn_ov001_021db508(0, var_r5)) {
        var_r6 = native_fn_ov001_021db438(0, var_r5);
    } else {
        var_r5 += 1;
        if (var_r5 < 3) {
            goto loop_1;
        }
    }
    if (var_r6 == 0) {
        var_r5_2 = 0;
loop_6:
        if (arg0 == native_fn_ov001_021db508(2, var_r5_2)) {
            var_r6 = native_fn_ov001_021db438(2, var_r5_2);
        } else {
            var_r5_2 += 1;
            if (var_r5_2 < 3) {
                goto loop_6;
            }
        }
    }
    return var_r6;
}
