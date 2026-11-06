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
extern u32 native_fn_ov001_021dc8b4();
u32 native_ov001_021dbb9c(u32 arg0, u32 arg1) {
    s32 var_r5;
    s32 var_r6;
    u32 var_r7;
    u32 var_r8;

    var_r7 = 1;
    var_r8 = arg0;
    if (var_r8 != 0) {
        var_r6 = 1;
    } else {
        var_r8 = native_fn_ov001_021db438(arg1, 0);
        var_r6 = 3;
    }
    var_r5 = 0;
    if (var_r6 > 0) {
loop_5:
        if ((M2C_FIELD(var_r8, u8 *, 0x31C) != 0) && (M2C_FIELD(var_r8, u8 *, 0x326) != 5)) {
            if (native_fn_ov001_021dc8b4((void *) var_r8) != 0) {
                var_r7 = 0;
            } else {
                var_r7 = 2;
                goto block_12;
            }
        } else {
block_12:
            var_r5 += 1;
            var_r8 += 0x440;
            if (var_r5 < var_r6) {
                goto loop_5;
            }
        }
    }
    return var_r7;
}
