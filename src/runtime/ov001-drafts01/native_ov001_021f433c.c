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
extern u32 native_fn_ov001_021db8d0();
u32 native_ov001_021f433c(void *arg0, u32 arg1) {
    s32 var_r0;
    s32 var_r4;
    s32 var_r5;
    u32 var_r6;
    u32 var_r7;

    var_r7 = arg1;
    var_r6 = 1;
    if (var_r7 == 0) {
        if (M2C_FIELD(arg0, u8 *, 0x31E) == 0) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        var_r7 = native_fn_ov001_021db438(var_r0, 0);
        var_r5 = 3;
    } else {
        var_r5 = 1;
    }
    var_r4 = 0;
    if (var_r5 > 0) {
loop_7:
        if ((native_fn_ov001_021db8d0((void *) var_r7) != 0) && (M2C_FIELD(var_r7, s8 *, 0x1E4) == 4)) {
            var_r6 = 0;
        } else {
            var_r4 += 1;
            var_r7 += 0x440;
            if (var_r4 < var_r5) {
                goto loop_7;
            }
        }
    }
    return var_r6;
}
